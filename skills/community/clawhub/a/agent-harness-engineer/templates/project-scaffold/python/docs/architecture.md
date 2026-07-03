# 架构文档

## 系统架构

```
+-------------------+
|     User Input    |
+-------------------+
          |
          v
+-------------------+
|   Agent Core      |
|  (状态机 + 循环)   |
+-------------------+
          |
    +-----+-----+
    |           |
    v           v
+--------+  +--------+
|  LLM   |  | Tools  |
| Client |  |Registry|
+--------+  +--------+
    |           |
    v           v
+--------+  +--------+
|Session |  |Permission|
| Manager|  | Manager  |
+--------+  +--------+
    |           |
    v           v
+--------+  +--------+
| Memory |  |Sandbox  |
| Manager|  | Manager |
+--------+  +--------+
```

## 核心组件

### Agent Core

Agent的核心循环，负责：
- 接收用户输入
- 调用LLM生成响应
- 执行工具调用
- 管理会话状态

### LLM Client

抽象的LLM客户端，支持多供应商：
- Anthropic (Claude)
- OpenAI (GPT)
- Azure OpenAI
- 本地模型 (Ollama/vLLM)

### Tool Registry

工具注册表，管理所有可用工具：
- 文件操作工具
- 网络请求工具
- 浏览器工具
- 自定义工具

### Permission Manager

权限管理器，控制Agent的操作范围：
- 权限规则配置
- Hook系统
- 沙箱管理

### Session Manager

会话管理器，实现不可变的会话日志：
- 会话创建和恢复
- 事件持久化
- 会话历史查询

### Memory Manager

记忆管理器，实现短期和长期记忆：
- 短期记忆（当前会话）
- 长期记忆（持久化存储）
- 记忆整合

## 数据流

```
User Input
    |
    v
+---------------+
| Agent Core    |
+---------------+
    |
    v
+---------------+
| LLM Client    |
+---------------+
    |
    +---> Text Response
    |
    +---> Tool Calls
            |
            v
        +---------------+
        | Tool Registry |
        +---------------+
            |
            v
        +---------------+
        | Permission    |
        | Manager       |
        +---------------+
            |
            v
        +---------------+
        | Sandbox       |
        | Manager       |
        +---------------+
            |
            v
        Tool Results
            |
            v
        +---------------+
        | Session       |
        | Manager       |
        +---------------+
            |
            v
        +---------------+
        | Memory        |
        | Manager       |
        +---------------+
```
