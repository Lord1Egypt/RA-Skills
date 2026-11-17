---
name: evolver-auth-troubleshoot
description: Diagnose and fix EvoMap Evolver Hub authentication failures (HTTP 403 node_secret_invalid / unauthorized). Use when evolver solidify/sync fails with 403, node_secret_invalid, or unauthorized errors.
---

# Evolver Auth Troubleshoot

排查 EvoMap Evolver Hub 认证失败（403 `node_secret_invalid` / `unauthorized`）。

## 症状

- `evolver solidify` 报 `hub_solidify_verification_denied: HTTP 403 node_secret_invalid`
- `evolver sync` / `sync.js` 报 `unauthorized`
- heartbeat / 资产发布失败

## 诊断步骤

1. **对比凭据一致性**（hash 对比，不打印 secret）
   - `grep A2A_NODE_ID .env` vs `cat ~/.evomap/node_id`
   - `grep A2A_NODE_SECRET .env | md5sum` vs `md5sum ~/.evomap/node_secret`
   - 不一致 = 凭据过期或节点已重新注册（以 `~/.evomap/` 为准）
2. **检查 OAuth token 是否过期**：`~/.evomap/oauth_token.json` 的 `expires_at`
3. **检查节点是否换过**：`.env` 的 `A2A_NODE_ID` 与 `~/.evomap/node_id` 不同 = 节点重新注册过

## 修复

1. 把 `~/.evomap/` 的 node_id / node_secret 同步进 `.env` 的 `A2A_NODE_ID` / `A2A_NODE_SECRET`
2. 重新授权：`evolver login` → 浏览器打开 `https://evomap.ai/device?user_code=XXX` → 输入设备码
3. 验证：`evolver solidify --dry-run`

## 离线回退（不需要 Hub 时）

- 注释/删除 `.env` 中的 `A2A_HUB_URL` / `A2A_NODE_ID` / `A2A_NODE_SECRET`
- evolver 全离线运行，solidify 不再需要 Hub 验证
- 代价：失去 skill store / worker pool / 资产发布等网络功能

## 脚本

```bash
node index.js        # 自动诊断，输出对比结果和修复指引
```

## 注意

- 从不打印 secret 明文（只输出 hash）
- 修改 `.env` 前先备份
