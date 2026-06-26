# 飞书 Probe 优化

检测并优化飞书扩展的 probe 缓存配置，减少 API 调用次数。

## 问题背景

OpenClaw 的飞书扩展在每次健康检查时会调用飞书 Bot API `/open-apis/bot/v3/info` 来验证连接状态。健康检查每分钟执行一次。

> **飞书免费额度**：每月 50,000 次（2026年3月）

### 默认配置

| 状态 | 缓存时间 |
|------|---------|
| 成功 | 10 分钟 |
| 失败 | 1 分钟 |

### 默认情况下的 API 调用量

假设配置了 N 个飞书账号：

- 每天调用：N × 24 × 60 = N × 1,440 次
- 每月调用：N × 43,200 次

如果配置 3 个飞书账号，每月调用 **129,600 次**，很容易超过飞书免费配额。

## 优化方案

将缓存时间调整为更长间隔：

| 状态 | 默认时间 | 优化后时间 |
|------|---------|-----------|
| 成功 | 10 分钟 | **24 小时** |
| 失败 | 1 分钟 | **1 小时** |

### 优化后的 API 调用量

- 每天调用：N × 1 次 = N 次
- 每月调用：N × 30 次

3 个账号：每月仅 **90 次**，节省 **99.93%**。

## 新增飞书账号

每增加一个飞书账号，每 24 小时会增加 1 次 API 调用（成功情况下）。配置本身无需修改，缓存机制自动适配所有账号。

| 账号数 | 每天调用 | 每月调用 |
|--------|---------|---------|
| 1 | 1 | 30 |
| 3 | 3 | 90 |
| 5 | 5 | 150 |
| 10 | 10 | 300 |

## 更新 OpenClaw 后

OpenClaw 大版本更新时，`extensions/feishu/src/probe.ts` 文件会被覆盖，缓存时间会恢复到默认值（10分钟/1分钟）。

**更新后需要：**

1. 重新修改 `probe.ts` 中的缓存配置
2. 执行全量编译：`pnpm build`
3. 重启服务：`systemctl --user restart openclaw-gateway`

详见下文「使用步骤」。

## 使用步骤

### 步骤 1：定位文件

```bash
find ~/.openclaw/workspace/openclaw/extensions/feishu/src -name "probe.ts"
```

### 步骤 2：修改配置

打开 probe.ts，找到这两行：

```typescript
const PROBE_SUCCESS_TTL_MS = 10 * 60 * 1000; // 10 minutes
const PROBE_ERROR_TTL_MS = 60 * 1000; // 1 minute
```

修改为：

```typescript
const PROBE_SUCCESS_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours
const PROBE_ERROR_TTL_MS = 60 * 60 * 1000; // 1 hour
```

### 步骤 3：全量编译

**重要：必须执行全量编译，禁止单扩展编译。**

```bash
cd ~/.openclaw/workspace/openclaw
pnpm build
```

### 步骤 4：验证编译产物

检查 `dist/extensions/` 目录是否包含全部扩展（feishu、telegram 等）。如果只剩 feishu，说明编译方式错误。

### 步骤 5：重启服务

```bash
systemctl --user restart openclaw-gateway
```

### 步骤 6：验证服务状态

```bash
systemctl --user status openclaw-gateway
```

确认服务正常运行（active (running)）。

## 为什么必须全量编译？

单扩展编译（如 `pnpm --filter feishu build`）会清空并覆盖 `dist/extensions/` 目录，导致其他扩展的编译产物被删除。

重启后服务会因配置校验失败而崩溃，并进入循环重启。

## 故障排查

### 服务重启后崩溃

```bash
journalctl --user -u openclaw-gateway -n 50
```

- 报错 `plugin not found`：dist 目录不完整，需要重新执行全量编译
- 报错 `Config invalid`：检查 openclaw.json 中的扩展配置

### 缓存未生效

确认修改的是 `extensions/feishu/src/probe.ts`（源码），不是 `dist/extensions/feishu/probe.js`（编译产物）。

## 前后对比

| 指标 | 优化前（3账号） | 优化后（3账号） | 节省 |
|------|----------------|----------------|------|
| 每天调用 | 4,320 次 | 3 次 | 99.93% |
| 每月调用 | 129,600 次 | 90 次 | 99.93% |
| 每年调用 | 1,555,200 次 | 1,095 次 | 99.93% |

## 更多信息

- 飞书 Bot API 文档：https://open.feishu.cn/document/server-docs/bot-v3/bot-info
- OpenClaw 飞书扩展：https://docs.openclaw.ai/channels/feishu
