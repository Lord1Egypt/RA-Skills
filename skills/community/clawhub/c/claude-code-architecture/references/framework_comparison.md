# Agent 框架架构对比

> 从公开资料分析的主流 Agent 框架设计模式对比

---

## 对比矩阵

| 维度 | Claude Code 风格 | OpenAI Agents SDK | LangChain/LangGraph | 本模板 |
|------|-----------------|-------------------|---------------------|--------|
| **工具权限** | Fail-closed 门控 | 声明式 guardrails | 回调链 | 五级权限门控 |
| **工具加载** | 按需索引+完整加载 | 全量注册 | 全量注册 | 两阶段懒加载 |
| **上下文管理** | 五级压缩 | 自动摘要 | 记忆组件 | 五级可配置压缩 |
| **并发模型** | 读写分离 | 异步图执行 | 图状态机 | ReadWriteScheduler |
| **安全边界** | 沙箱+权限 | 输入/输出 guard | 中间件 | 钩子+审计 |

---

## 各框架详析

### Claude Code 风格
- **核心思想**: Harness > Model，框架层承担安全与编排
- **权限模型**: 工具级权限 + 用户确认门控 + sandbox
- **特点**: 激进压缩（五级）、工具 system prompt 动态注入

### OpenAI Agents SDK
- **核心思想**: Agent = LLM + tools + handoffs
- **权限模型**: Input/output guardrails + 声明式 safety checks
- **特点**: Agent 间 handoff、tracing 内建、轻量级

### LangChain/LangGraph
- **核心思想**: Chain/Graph 作为编排原语
- **权限模型**: Callback middleware + 自定义检查
- **特点**: 生态丰富、学习曲线陡峭、状态管理强

---

## 选择建议

| 场景 | 推荐 |
|------|------|
| 需要严格控制工具权限 | 本模板 A + Claude Code 风格 |
| 多 Agent 协作 + handoff | OpenAI Agents SDK |
| 复杂工作流 + 状态管理 | LangGraph |
| Token 敏感 + 大量工具 | 本模板 B：工具按需加载 |
| 高并发工具调用 | 本模板 D：读写分离 |
