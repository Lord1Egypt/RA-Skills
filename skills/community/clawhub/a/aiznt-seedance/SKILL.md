---
name: aiznt-seedance
description: >
  即梦 Seedance 文生视频：豆包 Seedance 系列模型，content 数组格式。Use when: 用户指定 doubao-seedance 模型与多段文本/媒体内容。
metadata:
  openclaw:
    primaryEnv: TS_TOKEN
    requires:
      env:
        - AIZNT_PROXY_URLS
---

# Seedance 视频 (aiznt-seedance)

本技能封装 **即梦 Seedance** 异步视频管线：向 `seedance_content_generation_tasks` 提交包含 `model` 与 `content` 数组的请求体，再用 `seedance_content_generation_tasks_fetch` 轮询任务状态。认证与天树其它代理技能相同，使用 **Bearer TS_TOKEN**。

## 前置条件

- TsClaw **Skills** 中已为本技能配置 `TS_TOKEN` 与 `AIZNT_PROXY_URLS`（推荐一键「同步天树凭证」）。
- `AIZNT_PROXY_URLS` 解析后须包含：

| 键名 | 说明 |
|------|------|
| `seedance_content_generation_tasks` | POST 创建任务 |
| `seedance_content_generation_tasks_fetch` | GET 查询；URL 模板中 `{task_id}` 由脚本替换 |

## 请求体形状（概要）

上游通常要求：

- `model`：如 `doubao-seedance-1-0-pro-250528`（以你环境可用模型名为准）。
- `content`：对象数组，元素含 `type`（如 `text`）与 `text` 等字段；具体嵌套规则以火山 / 豆包当前文档为准。

示例（仅作结构参考）：

```bash
node scripts/seedance.js submit --body '{
  "model": "doubao-seedance-1-0-pro-250528",
  "content": [
    { "type": "text", "text": "A person walking through neon-lit alley, cinematic" }
  ]
}'
```

提交成功后，从响应中取出任务标识，再执行：

```bash
node scripts/seedance.js fetch --task-id <任务ID>
```

## 轮询建议

视频生成耗时较长，`fetch` 可能在多秒内返回 `processing` 类状态；由调用方（或 Agent）按间隔重复 `fetch`，直到成功、失败或超时。

## 故障排查

- **URL 未替换占位符**：确认 `seedance_content_generation_tasks_fetch` 的值含字面量 `{task_id}`，且与脚本中 `expandUrl` 一致。
- **业务 code 非 0**：`client.js` 会将网关包装的错误信息抛出，请根据 message 调整模型名或配额。

## 文件说明

- `scripts/seedance.js`：CLI（submit / fetch）。
- `scripts/client.js`：读取环境变量、拼 URL、`Authorization` 头、JSON 解析。
