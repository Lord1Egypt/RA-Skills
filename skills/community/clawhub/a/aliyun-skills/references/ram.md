# RAM (Resource Access Management) Reference

RAM manages users, roles, and policies for Alibaba Cloud access control.

## Users

### List Users

```bash
aliyun ram ListUsers
```

```bash
aliyun ram ListUsers \
  --output 'cols=UserName,DisplayName,CreateDate' 'rows=Users.User[]'
```

### Get User Details

```bash
aliyun ram GetUser --UserName alice
```

### Create a User

```bash
aliyun ram CreateUser \
  --UserName alice \
  --DisplayName "Alice" \
  --Comments "Developer account"
```

### Delete a User

> ⚠️ Detach all policies and delete access keys first.

```bash
aliyun ram DeleteUser --UserName alice
```

### Create Login Password (Console Access)

```bash
aliyun ram CreateLoginProfile \
  --UserName alice \
  --Password "P@ssw0rd!" \
  --PasswordResetRequired true
```

### Manage Access Keys

```bash
# List access keys for a user
aliyun ram ListAccessKeys --UserName alice

# Create an access key
aliyun ram CreateAccessKey --UserName alice

# Delete an access key
aliyun ram DeleteAccessKey --UserName alice --UserAccessKeyId LTAI5xxxxxx
```

---

## Policies

### List Policies

```bash
# List custom policies
aliyun ram ListPolicies --PolicyType Custom

# List system (built-in) policies
aliyun ram ListPolicies --PolicyType System
```

```bash
aliyun ram ListPolicies --PolicyType Custom \
  --output 'cols=PolicyName,PolicyType,Description' 'rows=Policies.Policy[]'
```

### Get Policy Document

```bash
aliyun ram GetPolicy --PolicyName ReadOnlyAccess --PolicyType System
```

### Create a Policy

```bash
aliyun ram CreatePolicy \
  --PolicyName MyCustomPolicy \
  --PolicyDocument '{"Version":"1","Statement":[{"Effect":"Allow","Action":["oss:GetObject","oss:ListObjects"],"Resource":"acs:oss:*:*:my-bucket/*"}]}' \
  --Description "Read-only access to my-bucket"
```

### Delete a Custom Policy

```bash
aliyun ram DeletePolicy --PolicyName MyCustomPolicy
```

---

## Attach / Detach Policies

### Attach Policy to User

```bash
aliyun ram AttachPolicyToUser \
  --PolicyType System \
  --PolicyName AdministratorAccess \
  --UserName alice
```

### Detach Policy from User

```bash
aliyun ram DetachPolicyFromUser \
  --PolicyType System \
  --PolicyName AdministratorAccess \
  --UserName alice
```

### List Policies Attached to a User

```bash
aliyun ram ListPoliciesForUser --UserName alice
```

---

## Groups

### List Groups

```bash
aliyun ram ListGroups
```

### Create a Group and Add User

```bash
aliyun ram CreateGroup --GroupName Developers

aliyun ram AddUserToGroup --GroupName Developers --UserName alice
```

### Attach Policy to Group

```bash
aliyun ram AttachPolicyToGroup \
  --PolicyType System \
  --PolicyName ReadOnlyAccess \
  --GroupName Developers
```

---

## Roles

### List Roles

```bash
aliyun ram ListRoles
```

```bash
aliyun ram ListRoles \
  --output 'cols=RoleName,RoleId,Description' 'rows=Roles.Role[]'
```

### Get Role

```bash
aliyun ram GetRole --RoleName my-ecs-role
```

### Create a Role (for ECS to assume)

```bash
aliyun ram CreateRole \
  --RoleName my-ecs-role \
  --AssumeRolePolicyDocument '{"Statement":[{"Action":"sts:AssumeRole","Effect":"Allow","Principal":{"Service":["ecs.aliyuncs.com"]}}],"Version":"1"}' \
  --Description "Role for ECS instances"
```

### Attach Policy to Role

```bash
aliyun ram AttachPolicyToRole \
  --PolicyType System \
  --PolicyName AliyunOSSReadOnlyAccess \
  --RoleName my-ecs-role
```

### Delete a Role

> ⚠️ Detach all policies first.

```bash
aliyun ram DetachPolicyFromRole \
  --PolicyType System \
  --PolicyName AliyunOSSReadOnlyAccess \
  --RoleName my-ecs-role

aliyun ram DeleteRole --RoleName my-ecs-role
```

---

## Common System Policies

| Policy Name | Scope |
|-------------|-------|
| `AdministratorAccess` | Full access to all resources |
| `ReadOnlyAccess` | Read-only access to all resources |
| `AliyunECSFullAccess` | Full ECS access |
| `AliyunECSReadOnlyAccess` | Read-only ECS access |
| `AliyunOSSFullAccess` | Full OSS access |
| `AliyunOSSReadOnlyAccess` | Read-only OSS access |
| `AliyunRDSFullAccess` | Full RDS access |
| `AliyunVPCFullAccess` | Full VPC access |
| `AliyunRAMFullAccess` | Full RAM access |
