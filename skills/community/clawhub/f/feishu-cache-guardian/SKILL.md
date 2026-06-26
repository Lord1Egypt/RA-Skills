---
name: feishu-cache-guardian
description: 飞书缓存配置守护工具。用于检查和修复 OpenClaw 飞书插件的 probe.ts 缓存配置。当飞书 API 健康检查的缓存时间被重置为默认值时，自动修复为60分钟缓存，避免API配额被快速耗尽。使用场景：OpenClaw升级后、飞书插件被覆盖后、定期检查缓存配置是否正常。
---

# Feishu Cache Guardian - 飞书缓存守护

## 背景

OpenClaw 的飞书通道每分钟会执行一次健康检查，调用 `probeFeishu()` 函数获取机器人信息。如果没有缓存机制，每月会产生约 43,200 次 API 调用，远超飞书免费配额的 10,000 次/月。

郑工长的优化方案添加了缓存机制：
- 成功响应缓存 60 分钟
- 失败响应缓存 60 分钟

**问题**：每次 OpenClaw 升级都会覆盖 `probe.ts` 文件，导致优化失效。

## 功能

本技能提供自动检查和修复功能：
1. 检查 `probe.ts` 的缓存配置是否为 60 分钟
2. 如果被重置为默认值，自动修复
3. 修复后自动重启 Gateway 使配置生效

## 使用方法

### 手动检查/修复

```bash
node ~/.openclaw/workspace/skills/feishu-cache-guardian/scripts/check-and-fix.js
```

### 设置定时检查（推荐）

使用 OpenClaw 的 cron 功能，每天检查一次：

```bash
openclaw cron add \
  --name "feishu-cache-check" \
  --schedule "0 9 * * *" \
  --command "node ~/.openclaw/workspace/skills/feishu-cache-guardian/scripts/check-and-fix.js"
```

或在升级后立即检查：

```bash
openclaw cron add \
  --name "feishu-cache-post-upgrade" \
  --schedule "@reboot" \
  --command "sleep 30 && node ~/.openclaw/workspace/skills/feishu-cache-guardian/scripts/check-and-fix.js"
```

## 文件位置

- 脚本：`scripts/check-and-fix.js`
- 目标文件：`/opt/homebrew/lib/node_modules/openclaw/extensions/feishu/src/probe.ts`

## 缓存配置说明

修改的内容：
```typescript
// 修改前（默认）
const PROBE_SUCCESS_TTL_MS = 10 * 60 * 1000; // 10 minutes
const PROBE_ERROR_TTL_MS = 60 * 1000;        // 1 minute

// 修改后（优化）
const PROBE_SUCCESS_TTL_MS = 60 * 60 * 1000; // 60 minutes
const PROBE_ERROR_TTL_MS = 60 * 60 * 1000;   // 60 minutes
```

## 效果

- 优化前：43,200 次/月（单账号）
- 优化后：720 次/月（单账号）
- 减少比例：98.3%

## 注意事项

1. 每次 OpenClaw 升级后，probe.ts 可能被覆盖，需要重新应用优化
2. 建议设置定时检查任务，确保配置始终有效
3. 脚本会自动重启 Gateway，修复后立即生效
