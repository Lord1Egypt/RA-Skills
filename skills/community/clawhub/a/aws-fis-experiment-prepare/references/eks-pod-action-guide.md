# EKS Pod Action Guide

## Contents

- Scope (which actions this applies to)
- Official Documentation (required reading)
- Setup Requirements
  - 1. Kubernetes RBAC — Managed via CFN Custom Resource (Lambda)
  - 2. EKS Access Entry (for FIS Experiment Role)
  - 3. EKS Cluster Authentication Mode
  - 4. Pod Memory Stress: Threshold Calculation
  - 5. Pod Security Context
  - 6. Network Action Limitations
- Naming Constraints
- CFN Service Role Permissions
- IAM Role Name Length
- CFN Deployment Notes
- Cleanup

## Scope

When the FIS action is any of the following types, you **MUST** complete the setup
steps in this document before generating any configuration files:

- `aws:eks:pod-cpu-stress`
- `aws:eks:pod-delete`
- `aws:eks:pod-io-stress`
- `aws:eks:pod-memory-stress`
- `aws:eks:pod-network-blackhole-port`
- `aws:eks:pod-network-latency`
- `aws:eks:pod-network-packet-loss`

## Official Documentation (Required Reading)

Before generating any configuration files, you **MUST** call `aws___read_documentation` to read:
https://docs.aws.amazon.com/fis/latest/userguide/eks-pod-actions.html

## Setup Requirements

### 1. Kubernetes RBAC — Managed via CFN Custom Resource (Lambda)

K8s RBAC resources (ServiceAccount, Role, RoleBinding) are **automatically managed**
by a Lambda-backed CFN Custom Resource. **No manual `kubectl apply` is required.**

**Key design: unified, shared RBAC resources.**
All `aws:eks:pod-*` actions require the same K8s RBAC permissions. Therefore, RBAC
resources use **fixed, standardized names** per namespace — shared across all FIS
experiments targeting the same cluster/namespace:

| Resource | Fixed Name |
|---|---|
| ServiceAccount | `fis-sa` |
| Role | `fis-experiment-role` |
| RoleBinding | `fis-experiment-role-binding` |

The Lambda performs **idempotent create** (check-before-create) on stack creation,
and **skips deletion** of RBAC resources on stack delete (since other experiments
may still be using them).

The CFN template **MUST** include the following resources (in dependency order):

#### 1a. Lambda Execution Role

```yaml
FISRBACLambdaRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: !Sub 'fis-lambda-role-${RandomSuffix}'
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: lambda.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    Policies:
      - PolicyName: EKSAccess
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Effect: Allow
              Action:
                - eks:DescribeCluster
              Resource: !Sub 'arn:aws:eks:${AWS::Region}:${AWS::AccountId}:cluster/${EKSClusterName}'
```

#### 1b. Lambda Execution Role's EKS Access Entry

Lambda Role must be registered in EKS to operate K8s resources. Use
`AmazonEKSClusterAdminPolicy` to grant the Lambda full K8s admin permissions
(needed to create ServiceAccount, Role, RoleBinding):

```yaml
LambdaEKSAccessEntry:
  Type: AWS::EKS::AccessEntry
  DependsOn: FISRBACLambdaRole
  Properties:
    ClusterName: !Ref EKSClusterName
    PrincipalArn: !GetAtt FISRBACLambdaRole.Arn
    Username: fis-rbac-lambda
    Type: STANDARD
    AccessPolicies:
      - PolicyArn: arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy
        AccessScope:
          Type: cluster
```

#### 1c. Lambda Function (Inline Code)

Uses `ZipFile` inline Python code — no S3 deployment package needed.

**Idempotent behavior:**
- **Create/Update:** GET each resource first; only POST if it does not exist (409/AlreadyExists is also treated as success)
- **Delete:** Do nothing — RBAC resources are shared and must NOT be deleted when a single experiment stack is removed

```yaml
FISRBACLambdaFunction:
  Type: AWS::Lambda::Function
  DependsOn:
    - FISRBACLambdaRole
    - LambdaEKSAccessEntry
  Properties:
    FunctionName: !Sub 'fis-rbac-${RandomSuffix}'
    Runtime: python3.12
    Handler: index.handler
    Role: !GetAtt FISRBACLambdaRole.Arn
    Timeout: 60
    Code:
      ZipFile: |
        import boto3, base64, json, urllib.request, urllib.error, os, re, time
        from botocore.signers import RequestSigner
        import cfnresponse

        def get_eks_token(cluster_name, region):
            """Generate EKS Bearer Token with x-k8s-aws-id header (same as aws eks get-token output)"""
            session = boto3.session.Session()
            client = session.client('eks', region_name=region)
            cluster_info = client.describe_cluster(name=cluster_name)['cluster']
            endpoint = cluster_info['endpoint']
            ca_data = cluster_info['certificateAuthority']['data']

            sts_client = session.client('sts', region_name=region)
            service_id = sts_client.meta.service_model.service_id
            signer = RequestSigner(service_id, region, 'sts', 'v4',
                                   session.get_credentials(), session.events)
            params = {
                'method': 'GET',
                'url': f'https://sts.{region}.amazonaws.com/?Action=GetCallerIdentity&Version=2011-06-15',
                'body': {},
                'headers': {'x-k8s-aws-id': cluster_name},
                'context': {}
            }
            signed_url = signer.generate_presigned_url(params, region_name=region,
                                                        expires_in=60, operation_name='')
            token = 'k8s-aws-v1.' + base64.urlsafe_b64encode(signed_url.encode()).decode().rstrip('=')
            return endpoint, ca_data, token

        def k8s_request(method, path, endpoint, token, ca_data, body=None):
            """Call K8s API directly without kubectl"""
            import ssl, tempfile
            ca_bytes = base64.b64decode(ca_data)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.crt') as f:
                f.write(ca_bytes)
                ca_file = f.name
            ctx = ssl.create_default_context(cafile=ca_file)
            url = endpoint + path
            data = json.dumps(body).encode() if body else None
            req = urllib.request.Request(url, data=data, method=method)
            req.add_header('Authorization', f'Bearer {token}')
            req.add_header('Content-Type', 'application/json')
            try:
                with urllib.request.urlopen(req, context=ctx) as resp:
                    return resp.status, json.loads(resp.read())
            except urllib.error.HTTPError as e:
                return e.code, json.loads(e.read())
            finally:
                os.unlink(ca_file)

        def ensure_resource(get_path, post_path, body, endpoint, token, ca_data):
            """Idempotent create: GET first, POST only if 404"""
            status, resp = k8s_request('GET', get_path, endpoint, token, ca_data)
            print(f'GET {get_path} -> {status}: {json.dumps(resp)[:500]}')
            if status == 200:
                return  # already exists, skip
            status2, resp2 = k8s_request('POST', post_path, endpoint, token, ca_data, body)
            print(f'POST {post_path} -> {status2}: {json.dumps(resp2)[:500]}')
            if status2 not in (200, 201, 409):
                raise Exception(f'Failed to create resource at {post_path}: {status2} {json.dumps(resp2)[:300]}')

        def handler(event, context):
            props = event['ResourceProperties']
            cluster = props['ClusterName']
            namespace = props['Namespace']
            region = props['Region']
            # Fixed, standardized names — shared across all FIS experiments
            sa_name = 'fis-sa'
            role_name = 'fis-experiment-role'
            binding_name = 'fis-experiment-role-binding'

            try:
                endpoint, ca_data, token = get_eks_token(cluster, region)

                if event['RequestType'] in ('Create', 'Update'):
                    # 1. ServiceAccount (idempotent)
                    sa = {'apiVersion':'v1','kind':'ServiceAccount',
                          'metadata':{'name':sa_name,'namespace':namespace}}
                    ensure_resource(
                        f'/api/v1/namespaces/{namespace}/serviceaccounts/{sa_name}',
                        f'/api/v1/namespaces/{namespace}/serviceaccounts',
                        sa, endpoint, token, ca_data)

                    # 2. Role (idempotent)
                    role = {
                        'apiVersion':'rbac.authorization.k8s.io/v1','kind':'Role',
                        'metadata':{'name':role_name,'namespace':namespace},
                        'rules':[
                            {'apiGroups':[''],'resources':['configmaps'],
                             'verbs':['get','create','patch','delete']},
                            {'apiGroups':[''],'resources':['pods'],
                             'verbs':['create','list','get','delete','deletecollection']},
                            {'apiGroups':[''],'resources':['pods/ephemeralcontainers'],
                             'verbs':['update']},
                            {'apiGroups':[''],'resources':['pods/exec'],
                             'verbs':['create']},
                            {'apiGroups':['apps'],'resources':['deployments'],
                             'verbs':['get']}
                        ]
                    }
                    ensure_resource(
                        f'/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/roles/{role_name}',
                        f'/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/roles',
                        role, endpoint, token, ca_data)

                    # 3. RoleBinding (idempotent)
                    binding = {
                        'apiVersion':'rbac.authorization.k8s.io/v1','kind':'RoleBinding',
                        'metadata':{'name':binding_name,'namespace':namespace},
                        'subjects':[
                            {'kind':'ServiceAccount','name':sa_name,'namespace':namespace},
                            {'apiGroup':'rbac.authorization.k8s.io','kind':'User',
                             'name':'fis-experiment'}
                        ],
                        'roleRef':{'kind':'Role','name':role_name,
                                   'apiGroup':'rbac.authorization.k8s.io'}
                    }
                    ensure_resource(
                        f'/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings/{binding_name}',
                        f'/apis/rbac.authorization.k8s.io/v1/namespaces/{namespace}/rolebindings',
                        binding, endpoint, token, ca_data)

                elif event['RequestType'] == 'Delete':
                    # Do NOT delete RBAC resources — they are shared across experiments.
                    # Other experiment stacks in the same namespace may still need them.
                    pass

                cfnresponse.send(event, context, cfnresponse.SUCCESS,
                                 {'ServiceAccountName': sa_name})
            except Exception as e:
                cfnresponse.send(event, context, cfnresponse.FAILED, {}, str(e))
```

#### 1d. Custom Resource (Triggers Lambda)

RBAC resources use **fixed standardized names** — the same `fis-sa`,
`fis-experiment-role`, `fis-experiment-role-binding` are shared by all FIS
experiments in the same namespace. The Lambda checks if they already exist before
creating, so multiple stacks targeting the same cluster/namespace are safe.

```yaml
FISKubernetesRBAC:
  Type: Custom::FISKubernetesRBAC
  DependsOn:
    - FISRBACLambdaFunction
    - LambdaEKSAccessEntry
  Properties:
    ServiceToken: !GetAtt FISRBACLambdaFunction.Arn
    ClusterName: !Ref EKSClusterName
    Namespace: !Ref TargetNamespace
    Region: !Ref AWS::Region
```

#### 1e. FIS Experiment Template References Fixed ServiceAccount

The FIS experiment template uses the fixed ServiceAccount name `fis-sa`:

```yaml
FISExperimentTemplate:
  DependsOn:
    - FISKubernetesRBAC   # Must wait for RBAC to be ensured
  Properties:
    Actions:
      InjectFault:
        Parameters:
          kubernetesServiceAccount: fis-sa
```

### 2. EKS Access Entry (for FIS Experiment Role)

The FIS Experiment Role's Access Entry **MUST** specify `Username: fis-experiment`:

```yaml
EKSAccessEntry:
  Type: AWS::EKS::AccessEntry
  Properties:
    ClusterName: {CLUSTER_NAME}
    PrincipalArn: !GetAtt FISExperimentRole.Arn
    Username: fis-experiment    # CRITICAL: Must match User in RoleBinding
    Type: STANDARD
    # No AccessPolicies needed - permissions are granted via K8S RBAC
```

**Do NOT:**
- Do NOT bind `AmazonEKSClusterAdminPolicy` to the FIS Experiment Role (overly permissive)
- Do NOT use namespace-scoped AccessPolicy (use K8S RBAC instead)

### 3. EKS Cluster Authentication Mode

The cluster must use `API_AND_CONFIG_MAP` or `API` authentication mode:
```bash
aws eks describe-cluster --name {CLUSTER} \
  --query 'cluster.accessConfig.authenticationMode'
```

### 4. Pod Memory Stress: Threshold Calculation

**When the action is `aws:eks:pod-memory-stress`, you MUST explain to the user
and calculate the correct `percent` parameter value.**

The `percent` parameter in `aws:eks:pod-memory-stress` represents **additional
memory to consume on top of existing usage**, NOT the total memory utilization
target. However, users typically think in terms of "I want the pod's total
memory to reach X%".

**Workflow:**

1. **Ask the user** for their desired total memory utilization target (e.g.,
   "80%"). Inform the user: "The percentage you specify is the **total Pod
   memory threshold** you want to reach, not the additional memory to inject."

2. **Query current memory usage** of the target pod(s):
   ```bash
   kubectl top pods -n {NAMESPACE} -l {POD_LABEL_SELECTOR}
   ```
   Compare with the pod's memory limit (from `kubectl get pod -o jsonpath` or
   `kubectl describe pod`) to calculate current utilization percentage.

3. **Calculate the injection value:**
   ```
   injection_percent = target_percent - current_usage_percent
   ```
   Example: User wants 80% total, current usage is 30% → injection value = 50%

4. **Validate:**
   - If `injection_percent <= 0`, warn the user: current usage already meets
     or exceeds the target — no injection needed.
   - If `injection_percent > 100`, this is invalid — ask the user to verify
     the target.

5. **Set the parameter** in the experiment template:
   ```json
   "parameters": {
     "duration": "PT5M",
     "percent": "{injection_percent}"
   }
   ```

6. **Include in README.md** the calculation details so the user understands:
   - Target total memory: X%
   - Current pod memory usage: Y%
   - Injected memory stress: X% - Y% = Z%

### 5. Pod Security Context

The target Pod's `readOnlyRootFilesystem` must be `false`. All EKS Pod actions will
fail if the root filesystem is read-only.

### 6. Network Action Limitations

The following actions do NOT support AWS Fargate or bridge network mode:
- `aws:eks:pod-network-blackhole-port`
- `aws:eks:pod-network-latency`
- `aws:eks:pod-network-packet-loss`

These actions require the ephemeral container to have root privileges. If the Pod
runs as non-root, you must set securityContext individually for containers in the Pod.

## Naming Constraints

K8s resource name rules: max 253 characters, lowercase letters, numbers, and `-` only.

K8s RBAC resources use **fixed names** per namespace (not per stack):
- ServiceAccount: `fis-sa`
- Role: `fis-experiment-role`
- RoleBinding: `fis-experiment-role-binding`

These are shared across all FIS experiments in the same namespace — no stack-name
suffix needed.

## CFN Service Role Permissions

If deploying via CFN with `--role-arn`, the CFN service role needs these permissions
in addition to existing ones:

```json
{
  "Sid": "LambdaManagement",
  "Effect": "Allow",
  "Action": [
    "lambda:CreateFunction",
    "lambda:DeleteFunction",
    "lambda:GetFunction",
    "lambda:UpdateFunctionCode",
    "lambda:UpdateFunctionConfiguration",
    "lambda:InvokeFunction",
    "lambda:AddPermission",
    "lambda:RemovePermission",
    "lambda:TagResource",
    "lambda:UntagResource"
  ],
  "Resource": "arn:aws:lambda:*:*:function:fis-rbac-*"
},
{
  "Sid": "IAMPassRoleToLambda",
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": "arn:aws:iam::*:role/fis-*",
  "Condition": {
    "StringEquals": {
      "iam:PassedToService": "lambda.amazonaws.com"
    }
  }
},
{
  "Sid": "EKSAccessEntryManagement",
  "Effect": "Allow",
  "Action": [
    "eks:CreateAccessEntry",
    "eks:DeleteAccessEntry",
    "eks:DescribeAccessEntry",
    "eks:AssociateAccessPolicy",
    "eks:DisassociateAccessPolicy",
    "eks:ListAssociatedAccessPolicies"
  ],
  "Resource": "*"
}
```

## IAM Role Name Length

The Lambda Execution Role (`FISRBACLambdaRole`) uses `fis-lambda-role-{RandomSuffix}` and
the FIS Experiment Role (`FISExperimentRole`) uses `fis-role-{RandomSuffix}` — both use
short prefixes with `RandomSuffix` to stay well within the 64-char IAM role name limit.
See `references/slug-conventions.md` for the full naming table.

## CFN Deployment Notes

Before deployment, check if the environment requires `--role-arn`:
```bash
# Check if existing FIS-related stacks use a service role
aws cloudformation describe-stacks --region {REGION} \
  --query 'Stacks[?contains(StackName,`fis`)].{Name:StackName,Role:RoleARN}' \
  --output table
```

If a CFN service role exists in the environment, all deploy and delete operations
must include `--role-arn`.

## Cleanup

Deleting the CFN Stack handles cleanup of stack-owned resources:
1. Lambda is invoked with `RequestType: Delete` -> **does nothing** (RBAC resources are shared, not deleted)
2. Lambda Function is deleted
3. Lambda Execution Role is deleted
4. Lambda EKS Access Entry is deleted
5. FIS Experiment Template, FIS IAM Role, FIS EKS Access Entry are deleted (existing logic)

**K8s RBAC resources (`fis-sa`, `fis-experiment-role`, `fis-experiment-role-binding`)
are intentionally NOT deleted** — they are shared across all FIS experiments in the
namespace. If you want to manually clean them up after removing ALL experiments:

```bash
kubectl delete rolebinding fis-experiment-role-binding -n {NAMESPACE}
kubectl delete role fis-experiment-role -n {NAMESPACE}
kubectl delete serviceaccount fis-sa -n {NAMESPACE}
```

User only needs for stack cleanup:
```bash
aws cloudformation delete-stack --stack-name {STACK_NAME} --region {REGION} \
  ${CFN_ROLE_ARN:+--role-arn ${CFN_ROLE_ARN}}
aws cloudformation wait stack-delete-complete --stack-name {STACK_NAME} --region {REGION}
```

No manual `kubectl delete` is required for normal operations.
