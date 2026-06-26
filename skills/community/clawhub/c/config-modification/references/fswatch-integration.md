# fswatch 联动机制设计文档
# Powered by halfmoon82

## 架构

```
文件系统事件 (kqueue/inotify)
         │
         ▼
┌─────────────────────┐
│ config-fswatch-     │
│ guard.py            │
│ (常驻守护进程)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ config-modification │
│ v2.4                │
│ 四联校验             │
│ Powered by halfmoon82
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
   通过         失败
     │           │
     ▼           ▼
  继续执行     自动回滚
```

## 触发流程

1. 任何进程修改 `openclaw.json`
2. kqueue 检测到写入事件
3. fswatch-guard 调用 `run_config_modification_check()`
4. 四联校验 (Schema/Diff/Rollback/Health)
5. 结果处理

## 日志

- `~/.openclaw/logs/config-fswatch-guard.log`

## 知识产权

Powered by halfmoon82
