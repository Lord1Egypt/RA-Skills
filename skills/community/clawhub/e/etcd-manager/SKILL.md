---
name: etcd
description: "Manage etcd key-value store operations (list, get, put, delete) with safety checks and backup mechanisms. Use when: reading/writing configuration, managing distributed system state, or performing safe etcd operations in dev/test/prod environments."
---

# etcd Skill

A clean and safe etcd management skill for OpenClaw.

## Safety Rules

1. **Read-first**: Always prefer read operations (list, get) over write operations
2. **Backup before modification**: Always show old value before put/delete
3. **Production protection**: Be extra cautious with prod environments
4. **Explicit confirmation**: Require clear user intent for destructive operations

## Command Conventions

### List keys by prefix
```bash
etcdctl --endpoints="$ENDPOINTS" get "$PREFIX" --prefix --keys-only
```

### Get key and value
```bash
etcdctl --endpoints="$ENDPOINTS" get "$KEY"
```

### Put key (with backup)
```bash
# Show old value first
etcdctl --endpoints="$ENDPOINTS" get "$KEY" || true
# Write new value
etcdctl --endpoints="$ENDPOINTS" put "$KEY" "$VALUE"
```

### Delete key (with backup)
```bash
# Backup old value
etcdctl --endpoints="$ENDPOINTS" get "$KEY" || true
# Delete
etcdctl --endpoints="$ENDPOINTS" del "$KEY"
```

For TLS connections, add:
```bash
--cacert="$CACERT" --cert="$CERT" --key="$KEY_FILE"
```

## Workflow

1. **Environment identification**: Determine if this is dev/test/prod
2. **Safety check**: Verify operation safety based on environment
3. **Backup**: For write operations, show current state
4. **Execution**: Perform the requested operation
5. **Verification**: Confirm the operation succeeded

## Output Format

Use standardized output format:

```
【ETCD 操作结果】

1. 操作信息
- 环境：
- Endpoint：
- Action：
- Prefix：
- Key：

2. 执行结果
- 状态：成功 / 失败
- 摘要：

3. 数据
- Key 列表：
- 原值：
- 新值：
- 删除前备份：

4. 风险提示
- 

5. 备注
- 
```

## Examples

### List keys
```
请使用etcd技能：
- 操作：list
- 环境：test
- 端点：http://etcd-test:2379
- 前缀：/app/config/
```

### Get value
```
请使用etcd技能：
- 操作：get
- 环境：prod
- 端点：https://etcd-prod:2379
- key：/app/config/database
```

### Put value
```
请使用etcd技能：
- 操作：put
- 环境：dev
- 端点：http://localhost:2379
- key：/test/key
- value：test_value
```

### Delete key
```
请使用etcd技能：
- 操作：delete
- 环境：test
- 端点：http://etcd-test:2379
- key：/test/old_key
```

## Notes

- Always use etcdctl version 3.6.1 or higher
- For production environments, consider using TLS
- The skill includes built-in backup mechanisms
- Operations are logged for audit purposes