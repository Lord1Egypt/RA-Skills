---
name: checkpoints
description: Records full context of AI-generated code and binds it to git commits. When the agent writes and commits code, capture prompts, conversation history, reasoning steps, decision logic, and token/metadata, then associate that checkpoint with the commit. Use when committing AI-produced changes or when the user wants to save or audit why and how code was generated.
---

# Checkpoints

Checkpoints 用于**自动记录 AI 生成代码的完整上下文**，并与对应的**代码提交（Commit）**绑定，便于回溯、审计和复现“这段代码是怎么来的”。

---

## 何时使用

- 智能体编写并即将提交（或刚提交）代码时，需要把本次生成的上下文一并留存。
- 用户明确要求“把这次改动的依据/对话记录下来”“和 commit 绑在一起”。
- 需要事后查看某次提交对应的提示词、推理过程和决策逻辑时，本 Skill 指导如何生成和存放 checkpoint 数据。

---

## Checkpoint 应包含的内容

在生成或提交 AI 代码时，将以下信息与 commit 绑定：

| 内容 | 说明 |
|------|------|
| **提示词（Prompts）** | 用户或系统触发生成的那条（或几条）主要 prompt，可做脱敏。 |
| **对话记录** | 与本次改动相关的对话摘要或关键轮次（可精简为要点）。 |
| **推理步骤** | 模型/智能体的推理链：先做了什么判断、尝试了哪些方案、为何选当前实现。 |
| **决策逻辑** | 关键决策点（例如：为何用 A 库而非 B、为何采用这种结构）。 |
| **元数据** | 可选：Token 消耗量、模型/版本、时间戳、涉及文件列表等。 |
| **关联 Commit** | 明确对应的 commit hash（或 branch + 即将提交的说明），保证可追溯。 |

---

## 与 Commit 绑定的方式

- **方式一：独立 checkpoint 文件**  
  在仓库中维护 checkpoint 存储（例如 `.checkpoints/` 或 `docs/checkpoints/`），每个 commit 对应一个文件，命名包含 commit hash 或时间戳，便于通过 hash 查找。
- **方式二：Commit 消息或 tag**  
  在 commit message 中写简短摘要，并注明“详细上下文见 .checkpoints/<hash>.json”；或打 tag 指向该 commit，tag 名/描述中带 checkpoint 标识。
- **方式三：外部系统**  
  若有现成的 Checkpoints 工具或服务，按该工具的 API/CLI 上传上述内容，并在 commit message 或仓库内留一条引用（如 URL 或 id）。

按项目约定或用户指定选择一种方式，并保持一致。

---

## Checkpoint 文件结构建议

若用文件形式保存，可采用结构化格式（便于后续解析和展示），例如：

```json
{
  "commit": "abc123...",
  "timestamp": "ISO8601",
  "prompts": ["用户请求的原始或摘要 prompt"],
  "conversation_summary": "与本次改动相关的对话要点",
  "reasoning_steps": ["步骤1", "步骤2", "..."],
  "decisions": ["决策1及原因", "..."],
  "files_changed": ["path/a", "path/b"],
  "meta": {
    "model": "optional",
    "tokens_used": "optional",
    "agent_version": "optional"
  }
}
```

也可用 Markdown 书写，便于人工阅读，但需固定章节（Prompts、对话摘要、推理步骤、决策、元数据、Commit）。

---

## 工作流程（智能体侧）

1. **在准备提交或完成提交后**：判断本次改动是否主要由 AI 生成；若是，则生成 checkpoint 内容。
2. **组装内容**：从当前对话中提取或总结：提示词、相关对话、推理步骤、决策逻辑；若有 token/模型信息则填入 meta。
3. **绑定 commit**：若尚未提交，先执行提交，取得 commit hash；再写入 checkpoint 文件或调用外部工具，并确保文件名/引用中包含该 hash。
4. **不污染主流程**：checkpoint 文件可加入 `.gitignore` 若仅本地使用；若团队需要共享审计，则纳入版本库并提交。

---

## 使用原则

- **一致性**：同一仓库内固定用一种绑定方式和目录/命名规则。
- **隐私与脱敏**：若 prompt 或对话中含敏感信息，存盘前做脱敏或仅存摘要。
- **可追溯**：通过 commit hash 能从 checkpoint 反查到提交，或从提交找到对应 checkpoint。
