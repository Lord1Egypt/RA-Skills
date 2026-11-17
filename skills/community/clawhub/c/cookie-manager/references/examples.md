# 示例 - cookie-manager

> 来源: SKILL.md v3.0 示例章节

## 示例1: Cron定时保活

### 场景
Cron每2天自动执行Cookie保活检查

### 输入
```json
{
  "mode": "keep_alive",
  "tenant_id": ""
}
```

### 执行
```
python skills/cookie-manager/scripts/cookie_keeper.py --mode keep_alive
```

### 输出
```json
{
  "success": true,
  "data": {
    "total": 3,
    "valid": 2,
    "invalid": 1,
    "alerts_sent": 1,
    "token_manager_synced": true,
    "sync_status": {
      "env_file": {"unb_match": true},
      "global_config": {"unb_match": true}
    },
    "health_details": [
      {"tenant_id": "T01", "platform": "xianyu", "health_score": 85.0}
    ]
  },
  "error": null,
  "code": "COOKIE_MANAGER_OK"
}
```

## 示例2: Cookie批量失效应急

### 场景
检测到2个Cookie同时失效,启动降级运营模式

### 输入
```json
{
  "mode": "detect",
  "failed_cookies": [{"account": "account_1"}, {"account": "account_2"}],
  "total_cookies": 3
}
```

### 执行
```
python skills/cookie-manager/scripts/cookie_emergency_manager.py --mode detect --failed-cookies '[{...},{...}]' --total-cookies 3
```

### 输出
```json
{
  "success": true,
  "data": {
    "degraded_mode": true,
    "paused_tasks": ["matrix-publish", "xianyu-manager", "auto-delivery"],
    "backup_switched": 1,
    "manual_recovery_needed": 1,
    "alerts_sent": 1
  },
  "error": null,
  "code": "COOKIE_MANAGER_OK"
}
```
