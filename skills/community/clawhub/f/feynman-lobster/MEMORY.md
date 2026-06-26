# 费曼虾记忆架构

这个文件**不是主记忆存储**，只负责说明 OpenClaw 下的记忆分工。

## 文件分工

### `contracts.json`

结构化状态源：

- 契约本身
- clauses 进度
- resources
- supervisors
- last_active_at

### `USER_PROFILE.md`

跨项目持久的用户画像：

- 学习偏好
- 学习风格
- 背景信息

只存放跨项目仍然有价值的信息。

### `contract-memory/{contract_id}.md`

当前项目的摘要文件：

- 概念理解记录
- 知识盲区
- 阶段总结
- 完约记录

每个契约一个文件，避免不同项目互相污染。

### OpenClaw memory 插件

可检索的长期记忆：

- 历史解释片段
- 失败追问片段
- 关联对话上下文

## 原则

1. 不把用户层和项目层混在一个 Markdown 文件里。
2. 不把结构化状态写进叙事记忆文件。
3. 不把可检索对话历史手工维护到 Markdown 中，交给 memory 插件。
