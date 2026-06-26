---
name: aiznt-sora2
description: >
  Sora2 文生视频：通过天树代理提交生成任务并轮询结果。Use when: 用户指定 sora_video2、sora-2-pro 等模型生成短视频。
metadata:
  openclaw:
    primaryEnv: TS_TOKEN
    requires:
      env:
        - AIZNT_PROXY_URLS
---

# Sora2 视频 (aiznt-sora2)

本技能在 **TsClaw / OpenClaw** 技能目录下提供两个 Node 入口：`submit` 创建异步任务，`fetch` 按任务 ID 查询状态与产物。所有请求经天树下发的代理 URL 转发，需使用与天树对话一致的 **Bearer** 凭证。

## 前置条件

1. **TsClaw** 已登录天树账号，并在 **Skills** 页对本技能执行「同步天树凭证」或手动保存配置。
2. 环境变量（由应用写入 `skills.entries`，执行时映射为进程环境）：
   - `TS_TOKEN`：天树 `ts_` 前缀的对话令牌。
   - `AIZNT_PROXY_URLS`：JSON 对象字符串，至少包含本技能用到的两个键（见下文）。键名需与后端 `getAizntProxyByTokenUrls` 返回字段一致。

## 代理 URL 键

| 键名 | 用途 |
|------|------|
| `v2_videos_generations` | POST，提交文生视频请求体（prompt、model 等） |
| `v2_videos_generations_fetch` | GET，查询任务；模板中可含 `{task_id}`，脚本会替换为实际 ID |

若 URL 模板含 `{task_id}`，**不要**手写死任务号；先 `submit` 取回 ID，再传给 `fetch`。

## 命令示例

在项目根或技能目录下（保证 `node` 能加载 `scripts/`）：

```bash
# 1. 提交任务（body 为上游要求的 JSON，示例字段仅供参考，以实际模型文档为准）
node scripts/sora2.js submit --body '{"prompt":"A coffee cup on a wooden table, slow pan","model":"sora_video2"}'

# 2. 假设上一步返回中包含任务 id（字段名依上游封装可能为 id / task_id），查询进度
node scripts/sora2.js fetch --task-id <上一步任务ID>
```

`submit` 成功返回的 JSON 结构取决于天树网关与上游封装；若只看到嵌套在 `data` 内的字段，请以实际响应为准解析 `task_id`。

## 常见错误

- **401 / 缺少 TS_TOKEN**：未同步凭证或 `apiKey` 过期，请在 TsClaw 重新同步或更新天树登录。
- **缺少 AIZNT_PROXY_URLS 某键**：凭证接口未返回对应代理路径，需后端配置齐 `v2_videos_generations` 与 `v2_videos_generations_fetch`。
- **HTTP 4xx 于 submit**：请求体字段名、模型名与上游不一致；对照当前可用的 Sora2 模型列表调整 `model` 与 `prompt` 约束。

## 与 TsClaw 的对应关系

- Skills 配置里 **`apiKey`** 对应环境变量 **`TS_TOKEN`**（`primaryEnv: TS_TOKEN`）。
- **`env.AIZNT_PROXY_URLS`** 为整段 JSON 字符串；本技能运行时只需上述两个键的非空值。

## 维护说明

脚本使用 Node 18+ 全局 `fetch`，无额外 npm 依赖。修改代理行为时请同步更新 `scripts/client.js` 中的 `loadClient` / `fetchJson` 与本文档中的 URL 键表。
