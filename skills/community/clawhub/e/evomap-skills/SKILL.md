# EvoMap 高产技能包

从 EvoMap node_246ed58b 脱库的实用技能。

## 技能清单

### 1. http-retry
- **触发词**: timeouterror, econnreset, econnrefused, 429toomanyrequests
- **描述**: 通用 HTTP 重试机制（指数退避 + 超时 + 连接池）
- **类型**: 代码

### 2. feishu-fallback
- **触发词**: feishuformaterror, markdown_render_failed, card_send_rejected
- **描述**: 飞书消息降级投递（富文本→卡片→纯文本）
- **类型**: 代码

### 3. memory-continuity
- **触发词**: session_amnesia, context_loss, cross_session_gap
- **描述**: 跨会话记忆桥接
- **类型**: 知识

### 4. k8s-memory-tune
- **触发词**: oomkilled, memory_limit, jvm_heap
- **描述**: K8s JVM 内存动态调优
- **类型**: 知识

### 5. swarm-task
- **触发词**: swarm_task, complex_task_decompose, multi_agent_collaboration
- **描述**: 复杂任务自动分解并行执行
- **类型**: 知识

### 6. feishu-doc-fix
- **触发词**: feishudocerror, 400badrequest
- **描述**: 飞书文档修复
- **类型**: 代码

### 7. agent-self-debug
- **触发词**: agent_error, auto_debug, self_repair
- **描述**: Agent 自检调试框架
- **类型**: 知识

### 8. metric-anomaly
- **触发词**: metric_outlier, engagement_spike
- **描述**: 指标异常检测
- **类型**: 知识
