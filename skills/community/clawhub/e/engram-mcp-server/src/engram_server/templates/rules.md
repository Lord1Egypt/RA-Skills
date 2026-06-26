# 运作规则
在这里写工作流程中的关键规则和约束条件。

# 常见错误
在这里写常见失败案例、避坑指南。
建议包含：错误场景 -> 后果 -> 纠正动作。

# 记忆规则
- 用户提到的关键事实时 → capture_memory(category="user-profile", memory_type="fact")
  示例：基本信息、背景、约束条件
- 用户表达的偏好时 → capture_memory(category="preferences", memory_type="preference")
  示例：喜好、风格偏好、不喜欢的方式
- 用户做出的重要决定时 → capture_memory(category="decisions", memory_type="decision")
  示例：选择了某个方案、确定了某个方向
- 对话中的重要历史节点时 → capture_memory(category="history", memory_type="history")
  示例：完成了某个里程碑、发生了某件重要的事

## Onboarding
首次对话时，自然地了解以下信息并记录：
- （在此填写3-5个关键问题，引导 LLM 在首次对话中自然收集）
- 示例：用户的背景和目标 → capture_memory(category="user-profile", memory_type="fact")
- 示例：用户的核心需求或约束 → capture_memory(category="user-profile", memory_type="fact")

## 知识提取规则
- 对话中形成了完整的方法论或决策框架时 -> 主动询问用户是否存入知识库，确认后调用 add_knowledge
- 用户分享了某个领域的系统性经验时 -> 提议 add_knowledge
- 用户纠正了现有知识中的错误时 -> 提议用 add_knowledge 更新对应文件
