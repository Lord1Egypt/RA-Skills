---
name: ai-system-maintenance
version: 1.0.0
description: 系统健康检查和维护，自动检测并修复常见问题
---

# AI System Maintenance 🛠️

系统健康检查和维护技能。当用户提到系统维护、健康检查、修复系统、系统出问题时使用。

## 触发条件

用户询问：
- "系统还好吗"
- "检查一下系统"
- "系统出问题了"
- "维护一下系统"
- "修复系统"
- "系统卡住了"
- "网关/浏览器/飞书 有问题"

## 执行步骤

1. 运行维护脚本：
```bash
/home/admin/.openclaw/workspace/scripts/system-maintenance.sh
```

2. 查看输出，总结检查结果

3. 如有问题被修复，告知用户

4. 如一切正常，回复系统状态良好

## 日志位置

- 当日维护日志：`~/.openclaw/workspace/logs/maintenance-YYYY-MM-DD.log`
- Cron 日志：`~/.openclaw/workspace/logs/cron-maintenance.log`

## 相关文档

`~/workspace/SYSTEM_MAINTENANCE.md`
