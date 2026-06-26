---
name: deepseek-v4-reasoning-bug
description: "排查 DeepSeek V4-Pro 在 tool-call 模式下因 reasoning_content 字段缺失导致的 API 400 错误。适用场景：(1) DeepSeek V4-Pro 使用 thinking/reasoning 模式时遇到 400 error, (2) 报错内容为 'The reasoning_content in the thinking mode must be passed back to the API', (3) 与 OpenClaw/OpenAI-compatible 客户端集成时 multi-turn + tool call 场景下报错。包含触发条件、复现方法、临时 workaround、官方修复跟踪。"
metadata: {"openclaw":{"homepage":"https://github.com/openclaw/openclaw/pulls?q=reasoning_content+deepseek"}}
---

# DeepSeek V4-Pro reasoning_content Bug

## 使用方式

当报错文本中出现 `The reasoning_content in the thinking mode must be passed back to the API.`，优先把本技能当作 **协议兼容性 / 消息回放问题** 来排查，而不是先怀疑网络、余额或普通鉴权。

## 问题描述

V4-Pro 启用 thinking（推理）模式时，在**多轮对话 + tool call** 场景下，DeepSeek API 要求客户端的后续请求必须回传前一轮响应中的 `reasoning_content` 字段，否则返回 HTTP 400。

```
The reasoning_content in the thinking mode must be passed back to the API.
```

## 触发条件

| 场景 | 结果 |
|---|---|
| 单轮对话（无工具） | ✅ 正常 |
| 单轮对话（有工具定义） | ✅ 正常 |
| 多轮对话（无工具调用） | ✅ 正常 |
| **多轮对话 + 工具调用 (tool call)** | ❌ **400 报错** |
| 多轮对话 + 作为工具（tool）角色 | ❌ **400 报错** |

**核心触发条件：** Tool call 产生的 tool 角色消息之后，下一轮对话必须包含上一轮的 `reasoning_content`，否则报错。

## DeepSeek 的约束要求

- `reasoning_content` 字段必须存在（值可以是空字符串 `""`）
- `reasoning_content` 完全缺失 → 400
- `reasoning_content` 合并到 `content` 字段中 → 400（DeepSeek 只看字段名，不看内容位置）
- `reasoning_content: ""`（空字符串）→ ✅ 200 成功

**因此最小修复方案是：** 在回传给 DeepSeek 的 assistant 消息中，无条件添加 `reasoning_content: ""` 字段作为 fallback。

## 影响范围

- 任何使用 DeepSeek V4-Pro + thinking 模式的客户端都可能遇到
- OpenClaw 中：`convertMessages` 函数会过滤掉内容为空的 thinking block，导致 `reasoning_content` 字段完全缺失
- 不影响 V4-Flash（`reasoning: false`，不产生 `reasoning_content`）
- 不影响单轮对话场景

## 排查方法

### 1. 确认是否是此 bug

检查 API 响应 body 中是否包含：
```json
{
  "error": {
    "message": "The reasoning_content in the thinking mode must be passed back to the API."
  }
}
```

### 2. 确认触发场景

查看请求历史，确认是否有 assistant + tool_calls 消息后跟了 tool 角色消息。

### 3. 临时 workaround

如果必须在当前版本使用 V4-Pro + thinking，可以：
- 每次请求中手动向 assistant 消息添加 `reasoning_content: ""` 
- 或在消息处理管线中拦截 assistant 消息，无条件注入空 `reasoning_content`

### 4. 检查客户端版本

检查所使用的 DeepSeek SDK / 客户端版本是否已有修复。

## 临时决策建议

- 如果当前客户端未修复：不要把 V4-Pro thinking + tool-call 当作稳定主力链路
- 如果必须继续使用：优先采用“无条件补 `reasoning_content: ""`”的最小 fallback
- 如果是纯单轮或无工具场景：可继续验证，但不要把该结果外推到多轮 tool-call 场景

## 官方修复状态

| PR | 作者 | 描述 | 状态 |
|---|---|---|---|
| [#71105](https://github.com/openclaw/openclaw/pull/71105) | lsdsjy | DeepSeek 官方 provider 插件 + reasoning_content 回传修复 | Review 中 |
| [#71146](https://github.com/openclaw/openclaw/pull/71146) | snowzlm | replay DeepSeek reasoning_content on tool-turn history | Review 中 |

两个 PR 于 2026-04-24 提交。修复方案都涉及在 tool-turn 历史消息中回传 `reasoning_content` 字段。

## 复现方法

```python
import requests

# 1. 首次请求（带 thinking + tool calls）
response = requests.post("https://api.deepseek.com/v1/chat/completions", json={
    "model": "deepseek-v4-pro",
    "reasoning": {"effort": "low"},
    "messages": [
        {"role": "user", "content": "查询一下天气"}
    ],
    "tools": [{"type": "function", "function": {"name": "get_weather", ...}}]
})

# 2. 模拟 tool call 结果
data = response.json()
assistant_msg = data["choices"][0]["message"]

# 3. 下次请求不传 reasoning_content → 会 400
bad_request = requests.post("https://api.deepseek.com/v1/chat/completions", json={
    "model": "deepseek-v4-pro",
    "reasoning": {"effort": "low"},
    "messages": [
        {"role": "user", "content": "查询一下天气"},
        {
            "role": "assistant",
            "content": assistant_msg["content"],
            "tool_calls": assistant_msg["tool_calls"],
            # ❌ reasoning_content 缺失
        },
        {"role": "tool", "content": "晴，25°C", "tool_call_id": ...}
    ]
})
# → HTTP 400 ❌
```
