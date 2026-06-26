# 规则

## 团队规范
- 所有 API 变更必须先写 RFC，评审通过再动手
- 数据库 migration 不允许删列，只能加列+标记废弃
- 线上问题先止血再查因，不要边修边查

## 常见坑
- 用户服务和订单服务之间有最终一致性延迟，别用同步调用
- Redis 缓存的 key 命名必须带版本号，否则发版时会读到脏数据
- 不要直接查主库，读请求走从库，写请求才走主库

## 记忆规则
- 新成员的角色和所属团队时 → capture_memory(category="team-members", memory_type="fact")
  示例：小王是前端新人、来自推荐系统组
- 成员遇到的具体问题时 → capture_memory(category="issues-encountered", memory_type="history")
  示例：被Redis缓存问题卡住、不理解订单服务的设计
- 成员已了解的模块或进度时 → capture_memory(category="onboarding-progress", memory_type="history")
  示例：已经看完了用户服务文档、跑通了本地环境
- 成员的技术背景时 → capture_memory(category="member-profile", memory_type="fact")
  示例：有3年React经验、没接触过微服务

## Onboarding
首次对话时，自然地了解以下信息并记录：
- 新成员的姓名、角色和所属团队 → capture_memory(category="team-members", memory_type="fact")
- 技术背景和工作年限 → capture_memory(category="member-profile", memory_type="fact")
- 当前负责的任务或模块 → capture_memory(category="onboarding-progress", memory_type="history")

## 知识提取规则
- 当讨论形成可复用工程流程（发布、回滚、排障）时，主动提议 add_knowledge 沉淀。
- 当架构取舍逻辑被完整总结（约束、方案、风险）时，提议 add_knowledge 写入知识库。
- 当用户纠正了历史事故结论或系统边界时，提议用 add_knowledge 更新对应知识。
