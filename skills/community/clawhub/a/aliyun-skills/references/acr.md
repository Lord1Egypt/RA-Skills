# ACR (Container Registry) Reference

Product code: `cr`

## Personal Edition vs Enterprise Edition

| | Personal Edition | Enterprise Edition |
|---|---|---|
| Instance ID | `crpi-xxxx` (new) or none (legacy) | `cri-xxxx` |
| aliyun CLI support | ❌ Not supported | ✅ Full API support |
| Auth | Permanent password (set in console) | Temporary token or permanent password |
| Registry endpoint | `registry.cn-<REGION>.aliyuncs.com` (legacy) / `crpi-xxxx.cn-<REGION>.personal.cr.aliyuncs.com` | `<name>-registry.<REGION>.cr.aliyuncs.com` |

> **Personal Edition** 不支持通过 `aliyun cr` 命令管理，命名空间和仓库须在控制台操作。
> 以下命令均适用于 **Enterprise Edition (ACR EE)**，所有命令需要 `--InstanceId cri-xxxx`。

---

## Instance Management

### List ACR EE Instances

```bash
aliyun cr ListInstance --region cn-hangzhou
```

```bash
aliyun cr ListInstance --region cn-hangzhou \
  --output 'cols=InstanceId,InstanceName,InstanceStatus,InstanceEndpoint' \
  'rows=Instances.Instance[]'
```

### Get Instance Details

```bash
aliyun cr GetInstance --region cn-hangzhou --InstanceId cri-xxxx
```

### Get Instance Quota Usage

```bash
aliyun cr GetInstanceUsage --region cn-hangzhou --InstanceId cri-xxxx
```

---

## Authentication (Docker Login)

### Get a Temporary Token (Valid 1 Hour)

```bash
aliyun cr GetAuthorizationToken --region cn-hangzhou --InstanceId cri-xxxx
```

Login to Docker with the temporary token:

```bash
TOKEN=$(aliyun cr GetAuthorizationToken --region cn-hangzhou --InstanceId cri-xxxx \
  | jq -r '.AuthorizationToken')

docker login \
  --username=cr_temp_user \
  --password="$TOKEN" \
  myinstance-registry.cn-hangzhou.cr.aliyuncs.com
```

### Reset Permanent Login Password

```bash
aliyun cr ResetLoginPassword \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --Password 'NewP@ss123!'
```

---

## Namespaces

### List Namespaces

```bash
aliyun cr ListNamespace --region cn-hangzhou --InstanceId cri-xxxx
```

### Create a Namespace

```bash
aliyun cr CreateNamespace \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --NamespaceName my-namespace \
  --AutoCreateRepo true \
  --DefaultRepoType PRIVATE
```

### Delete a Namespace

```bash
aliyun cr DeleteNamespace \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --NamespaceName my-namespace
```

---

## Repositories

### List Repositories

```bash
aliyun cr ListRepository --region cn-hangzhou --InstanceId cri-xxxx
```

Filter by namespace:
```bash
aliyun cr ListRepository \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --RepoNamespaceName my-namespace \
  --PageSize 100
```

### Get Repository Details

```bash
aliyun cr GetRepository \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --RepoNamespaceName my-namespace \
  --RepoName my-app
```

### Create a Repository

```bash
aliyun cr CreateRepository \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --RepoNamespaceName my-namespace \
  --RepoName my-app \
  --RepoType PRIVATE \
  --Summary "My application image"
```

### Delete a Repository

```bash
aliyun cr DeleteRepository \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --RepoNamespaceName my-namespace \
  --RepoName my-app
```

---

## Image Tags

### List Tags

> Requires `RepoId`. Get it from `GetRepository` → `RepoId` field.

```bash
REPO_ID=$(aliyun cr GetRepository --region cn-hangzhou --InstanceId cri-xxxx \
  --RepoNamespaceName my-namespace --RepoName my-app | jq -r '.RepoId')

aliyun cr ListRepoTag \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --RepoId "$REPO_ID"
```

### Delete a Tag

```bash
aliyun cr DeleteRepoTag \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --RepoId "$REPO_ID" \
  --Tag v1.0.0
```

### Copy a Tag

```bash
aliyun cr CreateRepoTag \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --NamespaceName my-namespace \
  --RepoName my-app \
  --FromTag v1.2.3 \
  --ToTag latest
```

---

## Public Endpoint Management

### List Endpoints

```bash
aliyun cr ListInstanceEndpoint --region cn-hangzhou --InstanceId cri-xxxx
```

### Enable/Disable Public Internet Endpoint

```bash
# Enable
aliyun cr UpdateInstanceEndpointStatus \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --EndpointType Internet \
  --Enable true

# Disable
aliyun cr UpdateInstanceEndpointStatus \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --EndpointType Internet \
  --Enable false
```

### Add IP to ACL Whitelist (Public Endpoint)

```bash
aliyun cr CreateInstanceEndpointAclPolicy \
  --region cn-hangzhou \
  --InstanceId cri-xxxx \
  --EndpointType Internet \
  --Entry 203.0.113.0/24
```

---

## Full Push / Pull Workflow

```bash
# 1. Find instance
aliyun cr ListInstance --region cn-hangzhou

# 2. Login with temporary token
TOKEN=$(aliyun cr GetAuthorizationToken --region cn-hangzhou --InstanceId cri-xxxx \
  | jq -r '.AuthorizationToken')
docker login --username=cr_temp_user --password="$TOKEN" \
  myinstance-registry.cn-hangzhou.cr.aliyuncs.com

# 3. Tag image
docker tag myapp:latest \
  myinstance-registry.cn-hangzhou.cr.aliyuncs.com/my-namespace/my-app:v1.0

# 4. Push
docker push myinstance-registry.cn-hangzhou.cr.aliyuncs.com/my-namespace/my-app:v1.0

# 5. Pull (on another machine after login)
docker pull myinstance-registry.cn-hangzhou.cr.aliyuncs.com/my-namespace/my-app:v1.0

# 6. Use VPC endpoint to avoid public traffic (on ECS within same region)
docker pull myinstance-registry-vpc.cn-hangzhou.cr.aliyuncs.com/my-namespace/my-app:v1.0
```

---

## Registry Endpoint Formats

| Type | Format |
|------|--------|
| Personal Edition (legacy) | `registry.cn-<REGION>.aliyuncs.com` |
| Personal Edition (new) | `crpi-xxxx.cn-<REGION>.personal.cr.aliyuncs.com` |
| Enterprise Edition (public) | `<name>-registry.<REGION>.cr.aliyuncs.com` |
| Enterprise Edition (VPC) | `<name>-registry-vpc.<REGION>.cr.aliyuncs.com` |
