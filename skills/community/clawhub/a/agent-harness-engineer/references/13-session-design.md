# 会话设计：WAL 事件日志模式

> Session = Write-Ahead Log (WAL)
> 与数据库的 WAL 设计模式同源：Append-only、Immutable、Replayable、Single Source of Truth.

---

## 设计理念

### 为什么是 WAL？

传统的 Session 设计将"当前状态"存储在可变数据结构中，每次操作原地修改。问题：
- 无法回放历史 → 难以调试
- 崩溃时状态丢失 → 无法恢复
- 审计信息不完整 → 合规困难

WAL 模式将每次事件作为不可变记录追加写入，Session 状态 = WAL 的重放结果。

```
传统模式:  State { messages: [...], tools: [...] }  → 原地修改
WAL 模式:  Event log → 重放 → 构建 State
```

### 核心属性

| 属性 | 含义 | 实现方式 |
|---|---|---|
| **Append-only** | 不修改历史，只追加新事件 | JSONL 格式，逐行追加 |
| **Immutable** | 已写入的事件不可更改 | 文件权限 + 校验和 |
| **Replayable** | 可从头重放恢复状态 | 事件幂等设计 |
| **Single Source of Truth** | 所有组件从事件日志派生状态 | 无独立状态存储 |

---

## 5 种事件类型

### 事件分类

```
                    ┌─────────────────────┐
                    │     Session 事件     │
                    └──────────┬──────────┘
          ┌────────────┬──────┴──────┬────────────┐
          │            │             │            │
    用户侧事件    模型侧事件    工具侧事件    控制事件
          │            │             │            │
   user_message  assistant_text  tool_use     turn_start
                               tool_result   turn_end
```

### 事件 Schema

| 事件类型 | 必填字段 | 说明 |
|---|---|---|
| `user_message` | `{timestamp, uuid, content, role}` | 用户输入，role 固定为 "user" |
| `assistant_text` | `{timestamp, uuid, content, model, token_count}` | 模型生成的文本片段 |
| `tool_use` | `{timestamp, uuid, tool_name, arguments, parent_message_uuid}` | 工具调用声明 |
| `tool_result` | `{timestamp, uuid, success, output/error, tool_use_uuid}` | 工具执行结果 |
| `turn_start` | `{timestamp, uuid, turn_number, reason}` | turn 开始标记 |
| `turn_end` | `{timestamp, uuid, turn_number, reason, token_summary}` | turn 结束标记 |

其中 `reason` 字段枚举值：
- `complete`：正常完成
- `timeout`：超时中断
- `error`：异常错误
- `user_interrupt`：用户手动停止
- `compaction_trigger`：触发压缩

---

## 状态机 (State Machine)

```
                    ┌──────────┐
         创建 ─────→│   idle   │
                    └────┬─────┘
                         │ user_message 到达
                         ▼
                    ┌──────────┐
                    │ running  │←───── 多轮 tool_use/tool_result 循环
                    └────┬─────┘
              ┌─────┬────┴────┬──────┐
              │     │         │      │
          正常完成  超时     错误   暂停
              │     │         │      │
              ▼     ▼         ▼      ▼
           idle  expired    error  paused
             │
             │ 新消息到达
             ▼
          running (继续)
```

### 状态转换规则

| 当前状态 | 触发事件 | 新状态 | 条件 |
|---|---|---|---|
| `idle` | `user_message` | `running` | 无活跃 turn |
| `running` | `turn_end(reason=complete)` | `idle` | 模型返回最终响应 |
| `running` | `turn_end(reason=timeout)` | `expired` | 超过 turn 超时限制 |
| `running` | `turn_end(reason=error)` | `error` | 执行异常 |
| `running` | `pause_command` | `paused` | 用户手动暂停 |
| `paused` | `resume_command` | `running` | 用户手动恢复 |
| `expired` | 任何事件 | `expired` | 不可恢复，需新建会话 |
| `error` | `retry_command` | `running` | 从最后一个 turn_end 恢复 |

---

## JSONL 格式规范

### 格式定义

每行一个 JSON 对象，行与行之间以 `\n` 分隔。

```jsonl
{"type":"turn_start","timestamp":"2025-01-15T10:30:00.001Z","uuid":"a1b2...","turn_number":1,"reason":"user_initiated"}
{"type":"user_message","timestamp":"2025-01-15T10:30:00.002Z","uuid":"c3d4...","content":"创建一个 Python HTTP 服务","role":"user"}
{"type":"tool_use","timestamp":"2025-01-15T10:30:02.100Z","uuid":"e5f6...","tool_name":"write","arguments":{"path":"server.py","content":"..."},"parent_message_uuid":"g7h8..."}
{"type":"tool_result","timestamp":"2025-01-15T10:30:02.350Z","uuid":"i9j0...","success":true,"output":"File written: server.py","tool_use_uuid":"e5f6..."}
{"type":"assistant_text","timestamp":"2025-01-15T10:30:03.000Z","uuid":"k1l2...","content":"已创建 server.py...","model":"claude-4","token_count":{"input":150,"output":80}}
{"type":"turn_end","timestamp":"2025-01-15T10:30:03.001Z","uuid":"m3n4...","turn_number":1,"reason":"complete","token_summary":{"total_input":150,"total_output":80,"total_cost":0.003}}
```

### JSONL 的优势

| 特性 | JSONL | Binary Format | 关系数据库 |
|---|---|---|---|
| **追加友好** | ✅ 直接追加 | 需序列化 | 需 INSERT |
| **人类可读** | ✅ | ❌ | 部分 |
| **流式处理** | ✅ 逐行读取 | 需解码器 | 需游标 |
| **jq 可查询** | ✅ `jq 'select(.type=="tool_use")'` | ❌ | 需 SQL |
| **版本兼容** | ✅ 向前兼容 | 需版本协商 | Schema 迁移 |
| **存储效率** | 中等 | 高 | 高 |

---

## 重放与恢复

### 故障恢复流程

```
恢复入口: Harness 启动时检测到未完成的 Session

Step 1: 加载 Session 的 JSONL 文件
Step 2: 逐行重放到最后一个 turn_end
Step 3: 检查最后一个 turn_end.reason
  ├─ complete → Session 已完成，无需恢复
  ├─ timeout  → 从下一 turn 继续（原 turn 结果可能部分可用）
  ├─ error    → 通知用户选择 retry 或 abandon
  └─ (无 turn_end) → 最后一个 turn 未完成，重新执行
Step 4: 恢复后的 Harness 从 idle 状态开始接受新消息
```

### 负载迁移流程

```
迁移入口: 将 Session 从 Harness A 迁移到 Harness B

Step 1: Harness A 序列化：将整个 JSONL 文件作为迁移载荷
Step 2: 传输到目标 Harness B (通过共享存储或网络)
Step 3: Harness B 加载 + 重放 JSONL
Step 4: 验证重放后的状态与 Harness A 一致
Step 5: Harness A 标记为 migrated，拒绝后续请求
Step 6: Harness B 接管所有后续交互
```

### 调试重放

```
调试入口: 生产环境 Session 出现异常行为

Step 1: 导出生产 Session 的 JSONL 文件
Step 2: 在开发环境加载并重放
Step 3: 在关键事件处设置断点（turn_end、tool_use）
Step 4: 注入相同模型版本和参数
Step 5: 比较开发环境输出与生产输出
Step 6: 定位差异点 → 根因分析
```

---

## 双重超时机制

### Turn-level Timeout

| 参数 | 默认值 | 说明 |
|---|---|---|
| `turn_timeout` | 120s | 单轮最大执行时长 |
| `tool_timeout` | 30s | 单次工具调用最大时长 |
| `max_tool_calls_per_turn` | 25 | 单轮最大工具调用次数 |

超时行为：
- `turn_timeout` 触发 → 中断当前执行，记录 `turn_end(reason=timeout)`
- `tool_timeout` 触发 → 中断当前工具调用，返回 error result，继续 turn
- `max_tool_calls` 触发 → 强制完成 turn，发送用户消息通知

### Session-level Timeout

| 参数 | 默认值 | 说明 |
|---|---|---|
| `session_idle_timeout` | 600s | idle 状态最大等待时长 |
| `session_max_duration` | 3600s | 总会话最大时长 |

超时行为：
- `session_idle_timeout` 触发 → 状态切换为 expired，释放资源
- `session_max_duration` 触发 → 强制结束，发送用户消息通知，释放资源

---

## Session = 审计日志

WAL 模式的一个自然产物：Session 的事件日志本身就是完整的审计日志。

### 审计能力

| 审计需求 | 实现方式 |
|---|---|
| 谁在何时使用了什么工具 | `tool_use` 事件包含时间戳 + 工具名 |
| 每一轮模型返回了什么 | `assistant_text` 事件包含内容 + token |
| 哪些权限决策被做出 | 权限检查事件 (作为 tool_use 的子类型) |
| 操作是否成功 | `tool_result.success` 字段 |
| 错误发生的上下文 | `tool_result.error` + 前后的事件序列 |
| 会话的总成本 | 所有 `turn_end.token_summary` 累加 |

### 合规优势

- 完整：无遗漏，所有操作都记录在事件流中
- 不可篡改：Append-only + 校验和
- 可验证：第三方可重放验证
- 标准化：JSON Schema 定义，便于工具链处理

---

## 规模特定实现概要

### Minimal (~30 行)
```
核心: 内存中的 list，追加事件对象
没有持久化，进程退出即丢失
适用: 单次交互、不需要历史的场景
```

### Professional (~100 行)
```
核心: JSONL 文件，每次事件发生时 append 一行
实现要点:
  - 文件打开模式: a (append, 自动创建)
  - 每次写入后 flush (防崩溃丢失单行)
  - Session 创建时分配 UUID 作为文件名
  - 提供 load(session_id) 工厂方法从文件恢复
  - Session 过期后归档文件到 sessions/ 目录
```

### Enterprise (~300 行)
```
核心: 双写 - JSONL 文件 + PostgreSQL
实现要点:
  - JSONL 文件保持人类可读和快速重放
  - PostgreSQL 提供查询、聚合、审计检索
  - 异步写入：先写 JSONL (同步)，后写 DB (异步)
  - 一致性校验：定期比对 JSONL 和 DB 记录数
  - 压缩优化：满 1000 个 turn 后压缩历史 JSONL (gzip)
  - 事件去重：基于 uuid 幂等写入
```

---

⚠ **AI 构建提示**：

```
根据用户选择的规模实现 Session：

Minimal 级别：
  1. 创建 EventLog 类 (list-based)
  2. 提供 append(event_type, data) 方法
  3. 提供 replay() 方法遍历恢复状态
  4. 无需文件 I/O

Professional 级别：
  1. 创建 JSONLSession 类
  2. 构造函数中分配 UUID (uuid4)
  3. 每次事件触发时调用 _write_event() → 追加一行 JSON
  4. 实现类方法 load(session_id) 从文件恢复
  5. 实现 close() 方法（flush + 关闭文件句柄）
  6. 实现在 __del__ 或 context manager 中自动 close

Enterprise 级别：
  1. 扩展 Professional 实现，添加数据库写入
  2. 实现异步写入队列 (asyncio.Queue)
  3. 实现一致性校验作业（定时器）
  4. 添加压缩/归档策略
  5. 添加事件去重逻辑 (uuid set)

所有级别必须：
  □ 支持 replay() 方法重建状态
  □ 包含 timestamp 字段在每个事件中
  □ turn_start 和 turn_end 必须成对出现
  □ 提供当前状态查询 (is_idle, is_running, etc.)
```