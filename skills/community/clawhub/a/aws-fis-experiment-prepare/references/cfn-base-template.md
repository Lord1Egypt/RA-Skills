# CFN Base Template Reference

Defines the CloudFormation template skeleton shared by all FIS experiments.
Scenario-specific guides extend this base with additional resources.

## Contents

- Template Structure Overview
- Parameters
- IAM Role (FIS Experiment Role)
- CloudWatch Dashboard (skeleton)
- FIS Experiment Template (skeleton)
- Optional: Stop Condition Alarm
- Optional: EKS Access Entry (see also `eks-pod-action-prerequisites.md`)
- Outputs

## Template Structure Overview

Every FIS experiment CFN template contains, at minimum:

1. **Parameters** — `ExperimentName`, `RandomSuffix`, `TargetAZ` (if applicable).
2. **FIS Experiment Role** — IAM role assumed by the FIS service.
3. **CloudWatch Dashboard** — Monitoring widgets for the target service(s).
4. **FIS Experiment Template** — The experiment definition itself.
5. **(Optional) Stop Condition Alarm** — Only when the user provides one.
6. **(Optional) EKS Access Entry** — Only for `aws:eks:pod-*` actions.
7. **Outputs** — `ExperimentTemplateId`, `DashboardURL`, `RoleArn`.

Scenario-specific guides (AZ Power Interruption, SSM Automation, etc.) add
resources on top of this base — Lambda functions, Custom Resources, SSM
Documents, and so on.

## Parameters

```yaml
Parameters:
  ExperimentName:
    Type: String
    Default: '{SCENARIO_SLUG}-{TARGET_SLUG}[-{CONTEXT_SLUG}]-{RANDOM_SUFFIX}'
    Description: >-
      Unique experiment identifier. Includes a random suffix to prevent
      resource-name collisions across experiments sharing the same scenario
      and target. Passed via --parameter-overrides at deploy time.
  RandomSuffix:
    Type: String
    Default: '{RANDOM_SUFFIX}'
    Description: >-
      6-character random suffix (same value used in ExperimentName).
      Used for Lambda function naming to keep names short and globally unique.
  TargetAZ:
    Type: String
    Default: '{AZ_ID}'
    Description: 'Target Availability Zone'
```

## FIS Experiment Role

Build this role using AWS managed policies as the base, plus an inline policy
for permissions not covered by any managed policy.

**Managed policy lookup by action prefix:**

| FIS Action Prefix | Managed Policy to Attach |
|---|---|
| `aws:ec2:stop-instances`, `aws:ec2:terminate-instances`, `aws:ec2:api-*`, `aws:ec2:asg-*` | `AWSFaultInjectionSimulatorEC2Access` |
| `aws:rds:*` | `AWSFaultInjectionSimulatorRDSAccess` |
| `aws:network:*`, `aws:ec2:send-spot-instance-interruptions` | `AWSFaultInjectionSimulatorNetworkAccess` |
| `aws:ecs:*` | `AWSFaultInjectionSimulatorECSAccess` |
| `aws:eks:*` | `AWSFaultInjectionSimulatorEKSAccess` |
| `aws:ssm:*` | `AWSFaultInjectionSimulatorSSMAccess` |
| `aws:ssm:start-automation-execution` (generic API) | `AWSFaultInjectionSimulatorSSMAccess` + `iam:PassRole` (see `ssm-automation-generic-api-guide.md`) |
| `aws:ebs:*` | `AWSFaultInjectionSimulatorEC2Access` (EBS actions are covered by the EC2 policy) |
| `aws:elasticache:*` | *(no managed policy — use inline)* |
| `aws:s3:*` | *(no managed policy — use inline)* |

**Selection rule:** Attach only the managed policies required by the actions in
the experiment.

**Template pattern:**

```yaml
FISExperimentRole:
  Type: AWS::IAM::Role
  Properties:
    RoleName: !Sub 'fis-role-${RandomSuffix}'
    AssumeRolePolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Effect: Allow
          Principal:
            Service: fis.amazonaws.com
          Action: sts:AssumeRole
    ManagedPolicyArns:
      # Attach AWS managed FIS policies based on the actions used:
      # - arn:aws:iam::aws:policy/service-role/AWSFaultInjectionSimulatorEC2Access
      # - arn:aws:iam::aws:policy/service-role/AWSFaultInjectionSimulatorRDSAccess
      # - arn:aws:iam::aws:policy/service-role/AWSFaultInjectionSimulatorNetworkAccess
      # - arn:aws:iam::aws:policy/service-role/AWSFaultInjectionSimulatorECSAccess
      # - arn:aws:iam::aws:policy/service-role/AWSFaultInjectionSimulatorEKSAccess
      # - arn:aws:iam::aws:policy/service-role/AWSFaultInjectionSimulatorSSMAccess
    Policies:
      # Add inline policy only for permissions NOT covered by managed policies
      - PolicyName: FISExtraPermissions
        PolicyDocument:
          Version: '2012-10-17'
          Statement:
            - Sid: FISLogging
              Effect: Allow
              Action:
                - logs:CreateLogDelivery
                - logs:PutLogEvents
                - logs:CreateLogStream
              Resource: '*'
            # Add service-specific permissions as needed:
            # - Sid: ElastiCacheActions
            #   Effect: Allow
            #   Action:
            #     - elasticache:InterruptClusterAzPower
            #     - elasticache:DescribeReplicationGroups
            #   Resource: '*'
```

## CloudWatch Dashboard

Group widgets by service. Each service section typically includes three widgets:
availability/health, performance/throughput, and errors/latency.

```yaml
ExperimentDashboard:
  Type: AWS::CloudWatch::Dashboard
  Properties:
    DashboardName: !Sub 'fis-${ExperimentName}'
    DashboardBody: !Sub |
      {
        "widgets": [
          {
            "type": "text",
            "x": 0, "y": 0, "width": 24, "height": 1,
            "properties": {
              "markdown": "# FIS Experiment: ${ExperimentName} | Region: ${AWS::Region}"
            }
          },
          {
            "type": "metric",
            "x": 0, "y": 1, "width": 12, "height": 6,
            "properties": {
              "title": "{SERVICE} Availability",
              "metrics": [
                ["{NAMESPACE}", "{AVAILABILITY_METRIC}", "{DIM_NAME}", "{DIM_VALUE}"]
              ],
              "period": 60,
              "region": "${AWS::Region}"
            }
          },
          {
            "type": "metric",
            "x": 12, "y": 1, "width": 12, "height": 6,
            "properties": {
              "title": "{SERVICE} Performance",
              "metrics": [
                ["{NAMESPACE}", "{PERF_METRIC_1}", "{DIM_NAME}", "{DIM_VALUE}"],
                ["{NAMESPACE}", "{PERF_METRIC_2}", "{DIM_NAME}", "{DIM_VALUE}"]
              ],
              "period": 60,
              "region": "${AWS::Region}"
            }
          },
          {
            "type": "metric",
            "x": 0, "y": 7, "width": 12, "height": 6,
            "properties": {
              "title": "{SERVICE} Errors / Latency",
              "metrics": [
                ["{NAMESPACE}", "{ERROR_METRIC}", "{DIM_NAME}", "{DIM_VALUE}"]
              ],
              "period": 60,
              "region": "${AWS::Region}"
            }
          }
        ]
      }
```

## FIS Experiment Template

```yaml
FISExperimentTemplate:
  Type: AWS::FIS::ExperimentTemplate
  DependsOn:
    - FISExperimentRole
  Properties:
    Description: !Sub 'FIS Experiment: ${ExperimentName}'
    RoleArn: !GetAtt FISExperimentRole.Arn
    StopConditions:
      - Source: 'none'
    Tags:
      Name: !Ref ExperimentName
      Scenario: '{SCENARIO_TYPE}'
    Targets:
      # {targets definition}
    Actions:
      # {actions definition}
```

## Optional: Stop Condition Alarm

Include this resource **only when the user explicitly provides a stop condition**.
When included, also update `FISExperimentTemplate.StopConditions` to:

```yaml
StopConditions:
  - Source: aws:cloudwatch:alarm
    Value: !GetAtt StopConditionAlarm.Arn
```

and add `StopConditionAlarm` to the template's `DependsOn` list.

```yaml
StopConditionAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: !Sub 'fis-stop-${ExperimentName}'
    AlarmDescription: 'Stop FIS experiment if critical threshold breached'
    Namespace: '{METRIC_NAMESPACE}'
    MetricName: '{METRIC_NAME}'
    Statistic: '{STATISTIC}'
    Period: 60
    EvaluationPeriods: 1
    Threshold: '{THRESHOLD}'
    ComparisonOperator: '{COMPARISON}'
    TreatMissingData: breaching
```

## Optional: EKS Access Entry (for Pod Actions)

Include this resource **only for EKS pod-related FIS actions** (e.g.,
`aws:eks:pod-delete`, `aws:eks:pod-network-latency`, `aws:eks:pod-cpu-stress`).

**Prerequisite:** The EKS cluster must use authentication mode
`API_AND_CONFIG_MAP` or `API`. Full requirements and the companion
Lambda-backed RBAC resources are documented in
`references/eks-pod-action-prerequisites.md`.

```yaml
EKSAccessEntry:
  Type: AWS::EKS::AccessEntry
  DependsOn: FISExperimentRole
  Properties:
    ClusterName: '{EKS_CLUSTER_NAME}'
    PrincipalArn: !GetAtt FISExperimentRole.Arn
    Username: fis-experiment  # Must match the User in the K8s RoleBinding
    Type: STANDARD
    # No AccessPolicies — permissions are granted via K8s RBAC
```

## Outputs

```yaml
Outputs:
  ExperimentTemplateId:
    Description: 'FIS Experiment Template ID'
    Value: !Ref FISExperimentTemplate
  DashboardURL:
    Description: 'CloudWatch Dashboard URL'
    Value: !Sub 'https://${AWS::Region}.console.aws.amazon.com/cloudwatch/home?region=${AWS::Region}#dashboards:name=fis-${ExperimentName}'
  RoleArn:
    Description: 'FIS Execution Role ARN'
    Value: !GetAtt FISExperimentRole.Arn
```
