# 示例 - checkpoint-manager

> 来源: SKILL.md v1.0.0 (ARCH-5) 示例章节

## 示例1: 保存检查点并快速读取

### 场景
工作流执行完一步后保存检查点,后续通过缓存快速读取

### 输入
```json
{
  "action": "save",
  "workflow_id": "wf_001",
  "step_id": "step_1",
  "tenant_id": "default",
  "state_data": {"progress": 30, "last_url": "https://example.com", "items": [1, 2, 3]}
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "id": 1,
    "authority_source": "pg",
    "cache_written": true
  },
  "error": null,
  "code": null
}
```

### 后续快速读取
```json
// 输入
{"action": "cached_get", "workflow_id": "wf_001", "step_id": "step_1"}

// 输出
{
  "success": true,
  "data": {
    "found": true,
    "source": "sqlite",
    "state_data": {"progress": 30, "last_url": "https://example.com", "items": [1, 2, 3]},
    "backfilled": false
  },
  "error": null,
  "code": null
}
```

## 示例2: 崩溃恢复重建

### 场景
SQLite缓存文件损坏/丢失后,从PG权威源重建缓存

### 输入
```json
{
  "action": "rebuild",
  "tenant_id": "default"
}
```

### 输出
```json
{
  "success": true,
  "data": {
    "pg_read_count": 100,
    "deleted_before": 0,
    "rebuilt_count": 100,
    "elapsed_sec": 0.5
  },
  "error": null,
  "code": null
}
```
