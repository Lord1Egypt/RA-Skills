---
name: dify_8d_analyzer
description: 当用户问题以「调用 8D 报告分析助手」开头时，调用 Dify API 进行 8D 问题分析
metadata:
  openclaw.requires:
    bins: ["timeout", "curl", "jq"]
---

# 8D 报告分析助手

当用户发送以「调用 8D 报告分析助手」开头的消息时，自动调用 Dify API 进行分析。

## 触发条件

- 用户消息以 `调用 8D 报告分析助手` 开头
- 例如：`调用 8D 报告分析助手，帮我分析最近三个月的问题分布`

## 执行步骤

1. **提取问题**：去掉前缀 `调用 8D 报告分析助手`，保留后面的实际问题内容
2. **获取用户 ID**：从当前消息上下文的 sender_id 获取用户 open_id
3. **调用脚本**：使用 background 模式执行命令
   ```bash
   timeout 180 /home/gem/workspace/agent/scripts/dify_router.sh "用户完整消息（含前缀）" "用户open_id"
   ```
   **注意**：使用 `exec` 工具时设置 `background: true` 或 `yieldMs: 180000`，让 OpenClaw 自动等待完整执行
4. **返回结果**：将脚本输出（stdout）作为回复发送给用户

## 重要配置

**exec 执行超时设置**：
- `timeout`: 180 秒（确保 Dify 有足够时间处理）
- `yieldMs`: 180000（让 OpenClaw 等待 3 分钟再自动后台化）

## 示例

**用户发送**：
```
调用 8D 报告分析助手，帮我分析最近三个月反馈最多的问题分布
```

**处理**：
1. 提取问题：`帮我分析最近三个月反馈最多的问题分布`
2. 获取用户 ID：`ou_7e872e790d6c2b4c3cd363ccf6a70d98`
3. 执行：`exec(command: "timeout 180 /home/gem/workspace/agent/scripts/dify_router.sh ...", timeout: 180, yieldMs: 180000)`
4. 返回：Dify 的分析结果

## 注意事项

- Dify 可能需要 30-120 秒处理复杂分析，请耐心等待
- 如果脚本返回错误（如 `ERROR:` 开头），将错误信息告知用户
- 脚本会维护多轮对话会话，无需用户重复提供上下文
