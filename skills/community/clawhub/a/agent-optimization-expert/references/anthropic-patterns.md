# Anthropic 工程实践模式

## 1. Extended Thinking Pattern

Anthropic Claude 的核心优势是 extended thinking（扩展思考）模式。

### 使用场景
- 复杂问题分解
- 多步骤推理
- 代码架构设计
- 错误诊断与修复

### 实践要点
```
1. 在思考阶段明确列出假设
2. 对每个假设进行验证
3. 记录推理链条
4. 最终输出时提炼结论，隐藏中间过程
```

### OpenClaw 映射
- `thinking` 参数控制思考级别
- 复杂诊断任务启用 thinking 模式
- 子 Agent 使用 thinking 进行深度分析

## 2. Tool Use Best Practices

### 预检-执行-后检模式
```
预检: 验证输入参数、权限、依赖状态
执行: 调用工具，带超时和重试
后检: 验证结果完整性、一致性
```

### 错误处理策略
```
1. 捕获具体错误类型（非通用异常）
2. 分类处理：
   - 可重试：指数退避重试
   - 需修正：调整参数重试
   - 不可恢复：降级到备用方案
3. 记录错误模式到学习库
```

## 3. Multi-Agent Coordination

### 子 Agent 使用原则
```
- context="isolated"：新任务，无需上下文
- context="fork"：需要当前对话上下文
- runTimeoutSeconds：设置合理超时
- 使用 sessions_yield 等待完成，不轮询
```

### 通信模式
```
主 Agent → 子 Agent: sessions_spawn(task, taskName)
子 Agent → 主 Agent: 完成事件自动传递
主 Agent ↔ 子 Agent: sessions_send 进行中途交互
```

## 4. Prompt Engineering Patterns

### 结构化输出
```
使用明确的输出格式要求：
- JSON schema 定义
- Markdown 模板
- 明确的字段名称
```

### 角色分离
```
不同任务使用不同的角色提示：
- 诊断模式："你是一个系统诊断专家..."
- 修复模式："你是一个运维工程师..."
- 优化模式："你是一个性能调优专家..."
```

### 自反思模式
```
在关键决策后添加：
"在继续之前，请反思你的分析：
1. 是否遗漏了重要信息？
2. 假设是否合理？
3. 有没有其他可能的解释？"
```

## 5. Context Management

### 上下文优化
```
- 使用 memory_search 检索相关信息，而非全部加载
- 大型文件使用 offset/limit 分段读取
- 子 Agent 使用 lightContext 减少 token
- 定期清理过期的 session 状态
```

### Token 预算
```
诊断任务：< 5000 tokens
修复任务：< 10000 tokens
复杂分析：使用子 Agent 隔离
```

## 6. Safety & Guardrails

### 操作分级
```
L0 - 安全：读取文件、检查状态
L1 - 低风险：修改临时文件、更新日志
L2 - 中风险：修改配置、重启服务
L3 - 高风险：删除数据、修改核心配置

L0-L1: 自动执行
L2: 提示用户确认
L3: 必须用户明确授权
```

### 审计日志
```
所有 L2+ 操作记录到：
- learnings/error-log.md
- memory/YYYY-MM-DD.md
- 包含：操作时间、内容、原因、结果
```
