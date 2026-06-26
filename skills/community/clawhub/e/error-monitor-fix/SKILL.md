---
name: error-monitor-fix
description: 错误监控 - 扫描 JSON 日志、捕获 ERROR 级别错误、OpenClaw 系统级错误修复建议
version: 3.0.0
---

# Error Monitor Fix — 错误监控技能

**版本**: 2.3.0 (所有修复策略改为提示手动，不再执行文件系统修改)  
**创建日期**: 2026-03-23  
**更新日期**: 2026-04-14

---

## 📋 功能

实时监控 OpenClaw 运行日志中的 error 类型错误，自动追加到 `error.md`，并尝试自动修复。

---

## 📂 文件结构

```
skills/error-monitor-fix/
├── SKILL.md
├── skill.json
├── _meta.json               # ClawHub 元数据
└── scripts/
    ├── monitor-error.js     # 错误监控（JSON 日志解析 + 去重）
    └── auto-fix.js          # 自动修复（5 种策略）
```

---

## 🔧 修复策略

| 策略 | 匹配条件 | 动作 |
|------|---------|------|
| Gateway 重启（提示手动） | gateway/ws/连接错误 | ⚠️ 提示用户手动重启 |
| 端口释放（只读检查） | EADDRINUSE | 检查 node 监听端口 |
| 会话清理（只读检查） | INVALID_REQUEST | dry-run 检查 |

> 缓存清理、权限修复属于 dev/test/rule 子代理操作范畴，不属于本技能。

---

## 📊 Cron 任务

| 任务名 | 频率 | Job ID |
|--------|------|--------|
| 错误监控修复 | 每 5 分钟 | `176ecc83` |

---

## ⚠️ 注意事项

- 去重窗口：1 小时（避免同一错误重复报告）
- 日志格式：JSON 行格式
- 输出：追加到 `memory/error.md`
