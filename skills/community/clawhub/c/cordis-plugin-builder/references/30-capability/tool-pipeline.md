# 工具执行管线（Tool Execution Pipeline）（实测 2026-08，555 文档蒸馏）

> 一个模型发出的工具调用，从"请求"到"落盘结果"经过的完整阶段链。**写工具插件前必读**——
> 你的 `execute()` 只是管线中间一步，前后有守卫、审批、钩子、规范化、观察者。

## 1. 管线总览（ASCII 版 Mermaid）

```
assistant message 含 tool-call 块
        │
        ▼
  ┌─ tool/call（会话事件，执行前落盘）───────────────┐
  │                                                 │
  ▼                                                 │
tools/pre-execute  (waterfall) ── allow ──► guards  │
  │  hooks/权限/沙箱策略           │ 单调守卫(deny)   │
  ├─ deny ──► 跳过 body            │ 或 abstain      │
  └─ ask ──► ctx.approval 一次性审批─┘                 │
        │ allowed / rejected                        │
        ▼                                           │
tools/execute  (waterfall，around-dispatch)         │
  │  timeout/retry/metrics                          │
  ▼                                                 │
execute() body ──► fs/write-intent·edit-intent 门   │
  │  + 工具自有事件(todo/write, fs/observed...)      │
  ▼                                                 │
tools/post-execute (waterfall，accept/block/replace)│
  ▼                                                 │
规范化 + finalizeContent（无损快照，throw→isError）  │
  ▼                                                 │
tools/result（emit，冻结权威结果，监听失败被包含）     │
  ▼                                                 │
tool/result（会话事件，唯一模型可见结果）──────────────┘
```

## 2. 阶段顺序（9 步，严格有序）

| # | 阶段 | 模式 | 作用 |
|---|---|---|---|
| 1 | `tool/call` 会话事件 | 持久 | 执行前落盘，模型的请求记录 |
| 2 | `tools/pre-execute` | waterfall | allow/deny/ask 门；hooks/权限/沙箱；缺审批支持时 ask→deny |
| 3 | **单调守卫** | 注册函数 | deny 或 abstain；在 pre 允许之后运行；身份受保护 |
| 4 | `tools/execute` | waterfall | around-dispatch：timeout/retry/metrics；`next()` 调真实 body |
| 5 | `execute()` body | — | 工具本体；可触发 fs 意图门 + 工具自有事件 |
| 6 | `tools/post-execute` | waterfall | accept/block/replace/enrich 归一化结果 |
| 7 | 规范化 + `finalizeContent` | 注册表 | 无损快照（throw→isError）+ 仅内容不变式 |
| 8 | `tools/result` | emit | 同步观察冻结的权威结果；监听失败被包含 |
| 9 | `tool/result` 会话事件 | 持久 | 唯一模型可见结果，驱动 UI + 解阻塞 |

## 3. 关键机制（实测契约）

- **三个 waterfall + code-dispatch-log** 声明在 `ctx.tools`（ToolRuntime）上：
  - `tools/pre-execute(exec, next) → PreToolDecision`（allow/deny/ask）
  - `tools/execute(exec, next) → ToolExecutionResult`（around-dispatch）
  - `tools/post-execute(exec, result, next) → PostToolDecision`（accept/block/replace/enrich）
  - `tools/code-dispatch-log(dispatch, next)`：只改 run_code 子调用的**持久日志副本**，程序收到的是完整值
- **scope-filtered dispatch**：`this: Scoped<ToolRuntime>`——agent 作用域监听器只收该 agent 的调用。
- **executionMode**：`parallel`（可与兄弟并发）vs `exclusive`（独占地形成屏障）；只有精确 `true` 才算 parallel。
- **hooks 现实消费**：`hooks-claude-code` 把 PreToolUse/PostToolUse 映射到 pre/post 瀑布，委托 `next()` 合并上下文；`hooks-codex` 只 honor deny（无 ask）。

## 4. 对工具插件开发者的启示

1. **你的 `execute()` 不是全部**——模型看到的卡片由 `tools/result`→`tool/result` 驱动，展示与业务分离（对应 harness-integration.md 的 output.render）。
2. **守卫/审批不归你管**——`tools/pre-execute` 的 allow/deny/ask 由 hooks/权限/沙箱策略监听；工具自身不需要实现审批。
3. **结果会被规范化**——抛错被归一化为 `isError`，`finalizeContent` 强制仅内容不变式；返回 lossless JSON（对应"不序列化 live 数据"纪律）。
4. **想加策略（如审计/超时）** → 监听 `tools/pre-execute` 或包 `tools/execute`（见 events-catalog.md 的事件脑图）。
5. **保留名 `run_code`** 是 Code Mode 传输通道，普通工具别用。

## 5. 排障速查

| 现象 | 管线哪一步 |
|---|---|
| 工具被拒但没执行 | pre-execute deny / guards deny / approval rejected |
| 执行了但结果被改 | post-execute block/replace |
| 结果带 isError | execute body 抛错被规范化 |
| UI 卡未完成 | tool/result 未落盘（batch 未 settle） |
