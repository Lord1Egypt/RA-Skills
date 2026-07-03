# Phase 4: Agent核心循环

## 目标

设计健壮的Agent主循环——这是Agent系统的**心脏**。旧版 AgentCore.run() 存在严重缺陷：它没有真正的 `while True` 循环，首次工具调用后就 `return` 了结果。正确的设计需要：永不退出的循环、7个弹性恢复点、状态机、流式事件输出、会话事件日志。

---

## 设计原理

### 旧版设计的致命缺陷

```
# ❌ 错误的 AgentCore.run()
async def run(self, user_input: str) -> str:
    while True:
        response = await self.llm_client.chat(...)
        if response.tool_calls:
            results = await self._execute_tools(response.tool_calls)
            self.state.messages.append(format(results))
            continue          # 继续循环 —— 看起来没问题
        return response.content  # ❌ 首次无工具调用就退出！
```

**问题**：
- 如果 LLM 返回文本（无 tool_use），run() 立即返回，不再给 LLM 继续思考和调用工具的机会
- 错误恢复粗糙：一个 `except Exception` 包裹整个循环体，无法精细区分恢复策略
- 没有流式事件：调用方阻塞等待整个 `str` 结果，中间状态不可观察
- 没有状态机：无法暂停、续跑、超时控制
- 会话管理耦合在独立类中，缺少 WAL 语义

### 正确设计的核心原则

1. **永不退出**：`while True` 是 Agent 循环的绝对基础，不会有"自然结束"——只有达到终止条件才 `break`
2. **流式事件输出**：使用 `AsyncGenerator` yield 中间事件，调用方可以实时消费进度
3. **状态机驱动**：状态转换明确，每个 continue 站点检查当前状态
4. **7个弹性恢复点**：每种失败模式有专属的恢复策略，按严重程度渐进升级
5. **事件日志即真理**：会话事件以 append-only JSONL 形式写入，类比数据库 WAL

---

## 抽象接口层

### 1. 状态机定义

```
状态机图（Mermaid 伪代码）:

  ┌──────┐    用户输入     ┌─────────┐
  │ idle │ ───────────────→ │ running │
  └──────┘                  └─────────┘
     ↑                          │  │  │
     │      循环结束             │  │  │
     │  (session_reset)         │  │  │ 达到 max_turns / 超时
     │                          │  │  └──────────────────────→ ┌─────────┐
     │    Stop Hook 阻塞        │  │                            │ expired │
     │    ←─────────────────────┘  │                            └─────────┘
     │                             │
     │   API 不可恢复错误           │  手动暂停
     │   ←─────────────────────────┘  ────────────→ ┌────────┐
     │                                               │ paused │
     │   不可恢复异常                                  └────────┘
     │   ←──────────────────────────────────────────→ ┌───────┐
     │                                                │ error │
     └───────────────────────────────────────────────→ └───────┘
```

**状态枚举**（抽象类骨架）：

```python
class AgentState(Enum):
    IDLE       = "idle"      # 会话尚未启动，等待首次输入
    RUNNING    = "running"   # 循环正在执行
    PAUSED     = "paused"    # 被外部信号暂停（Stop Hook 触发后）
    EXPIRED    = "expired"   # 达到轮次上限或会话级超时
    ERROR      = "error"     # 不可恢复异常，会话终止
```

**State 对象**（伪代码——仅字段声明，非可运行的实现）：

```python
@dataclass
class AgentRunState:
    """Agent 运行时状态——每次迭代开始时解构，在 continue 站点重新赋值"""
    status: AgentState = AgentState.IDLE

    # 消息历史（不可变追加语义：每次 continue 站点应整体替换而非原地修改）
    messages: List[Dict[str, Any]] = field(default_factory=list)

    # 轮次控制
    turn_number: int = 0
    max_turns: int = 50
    session_started_at: float = 0.0       # time.monotonic()
    session_timeout_seconds: float = 600.0 # 会话级超时（企业级：双重超时）

    # 恢复标志（陷阱：每次 continue 站点必须重置！）
    has_attempted_reactive_compact: bool = False

    # 暂停信号
    pause_requested: bool = False
    resume_callback: Optional[Callable] = None

    # 错误追踪
    last_error_type: Optional[str] = None
    consecutive_errors: int = 0
    max_consecutive_errors: int = 3
```

### 2. AgentCore 抽象类

> **重要**：以下所有代码片段是**抽象骨架 + 伪代码**，不可直接复制运行。目的是展示接口签名、循环结构和7个 continue 站点的位置关系。

```
# ─── 抽象 AgentCore 骨架 ───
class AgentCore:
    """
    永不退出的 Agent 主循环。

    架构约束:
      - 状态: 单一 AgentRunState 实例，伪不可变（continue 站点必须整体重新赋值）
      - 输出: AsyncGenerator[AgentEvent, None] —— 每个中间状态作为一个事件 yield
      - 恢复: 7个 continue 站点覆盖所有已知失败模式
      - 日志: SessionEventLog 以 append-only JSONL 持久化，每个事件必须在前才能 yield 给调用方
    """

    state: AgentRunState
    event_log: SessionEventLog
    llm_client: BaseLLMClient          # 来自 Phase 2
    tool_registry: ToolRegistry        # 来自 Phase 3
    context_manager: ContextManager    # 来自 Phase 5
    stop_hooks: List[StopHook]         # 来自 Phase 6

    # ═══════════════════════════════════════════════════════════
    # 主循环（伪代码——展示结构而非可运行实现）
    # ═══════════════════════════════════════════════════════════
    async def run(self, user_input: str) -> AsyncGenerator[AgentEvent, None]:
        """
        永不退出的 Agent 主循环。

        Yield 事件类型:
          - TurnStartEvent     → 每轮开始
          - UserMessageEvent   → 首次用户输入已记录
          - AssistantTextEvent → LLM 返回文本增量（流式）
          - ToolUseEvent       → LLM 请求工具调用
          - ToolResultEvent    → 工具执行结果
          - TurnEndEvent       → 每轮结束
          - StateChangeEvent   → 状态转换（idle→running、running→paused 等）
          - ErrorEvent         → 恢复性错误（非致命）
        """

        # === 入口状态验证 ===
        if self.state.status != AgentState.IDLE:
            yield StateChangeEvent("Cannot start: agent is not IDLE")
            return

        self.state.status = AgentState.RUNNING
        self.state.session_started_at = time.monotonic()
        yield StateChangeEvent(old=IDLE, new=RUNNING)

        # 记录首次用户消息
        self.event_log.append(UserMessageEvent(content=user_input))
        self.state.messages = [*self.state.messages, {"role": "user", "content": user_input}]

        # ═══════════════════════════════════════════════════
        #  永不退出的主循环
        # ═══════════════════════════════════════════════════
        while True:
            # ── 0. 前置检查 ──
            # 状态检查：是否被外部暂停
            if self.state.pause_requested:
                self.state.status = AgentState.PAUSED
                yield StateChangeEvent(old=RUNNING, new=PAUSED)
                await self._wait_for_resume()
                self.state.status = AgentState.RUNNING
                yield StateChangeEvent(old=PAUSED, new=RUNNING)

            # 轮次上限检查
            if self.state.turn_number >= self.state.max_turns:
                self.state.status = AgentState.EXPIRED
                yield StateChangeEvent(old=RUNNING, new=EXPIRED, reason="max_turns_reached")
                break

            # 会话级超时检查（企业级：双重超时的外层）
            elapsed = time.monotonic() - self.state.session_started_at
            if elapsed > self.state.session_timeout_seconds:
                self.state.status = AgentState.EXPIRED
                yield StateChangeEvent(old=RUNNING, new=EXPIRED, reason="session_timeout")
                break

            # ── 1. 轮次开始 ──
            self.state.turn_number += 1
            turn_start = time.monotonic()
            self.event_log.append(TurnStartEvent(turn=self.state.turn_number))
            yield TurnStartEvent(turn=self.state.turn_number)

            try:
                # ── 2. 压缩管道（Phase 5 集成点）──
                # 这是 CONTINUE-SITE-1 的调用入口
                self.context_manager.compact(self.state.messages)
                if self.context_manager.was_compacted():
                    yield CompactionEvent(detail=self.context_manager.last_compaction_detail)
                    # 压缩完成后不退出循环，继续在同一轮发送请求

                # ── 3. 调用 LLM（流式）──
                # 轮次级超时包装（企业级：双重超时的内层）
                try:
                    async for chunk in self.llm_client.stream_chat(
                        messages=self.state.messages,
                        tools=self.tool_registry.get_definitions(),
                        timeout=self._turn_timeout(),
                    ):
                        # 流式输出文本块
                        if chunk.is_text:
                            self.event_log.append(AssistantTextEvent(content=chunk.delta))
                            yield AssistantTextEvent(content=chunk.delta)
                        # 累积完整响应
                        response = self._accumulate(chunk)

                except TurnTimeout:
                    # 单轮超时 —— 不算致命，给一次重试机会
                    self.state.consecutive_errors += 1
                    if self.state.consecutive_errors > self.state.max_consecutive_errors:
                        self.state.status = AgentState.ERROR
                        yield StateChangeEvent(old=RUNNING, new=ERROR, reason="turn_timeout_exhausted")
                        break
                    yield ErrorEvent(type="turn_timeout", turn=self.state.turn_number)
                    continue  # ← 回到循环顶部重试

                # ── 4. 后处理响应 ──
                self.event_log.append(AssistantTextEvent(content=response.text, is_final=True))

                # ── 5. 处理 tool_use ──
                if response.has_tool_uses:
                    for tool_call in response.tool_uses:
                        self.event_log.append(ToolUseEvent(
                            tool_name=tool_call.name,
                            tool_input=tool_call.input,
                            tool_use_id=tool_call.id,
                        ))
                        yield ToolUseEvent(tool_call)

                    # 执行工具
                    tool_results = []
                    for tool_call in response.tool_uses:
                        try:
                            result = await self.tool_registry.execute(
                                name=tool_call.name,
                                arguments=tool_call.input,
                            )
                            tool_results.append(result)
                            self.event_log.append(ToolResultEvent(
                                tool_use_id=tool_call.id,
                                content=result.content,
                                is_error=result.is_error,
                            ))
                            yield ToolResultEvent(result)
                        except Exception as tool_error:
                            tool_results.append(ErrorResult(tool_call.id, str(tool_error)))
                            self.event_log.append(ToolResultEvent(
                                tool_use_id=tool_call.id,
                                content=str(tool_error),
                                is_error=True,
                            ))

                    # 将工具结果追加到消息历史
                    # 使用伪不可变语义：整体替换而非原地 push
                    for tr in tool_results:
                        self.state.messages = [
                            *self.state.messages,
                            {"role": "user", "content": str(tr.content)},
                        ]

                    # ★ CONTINUE-SITE-7: 正常工具执行完成
                    # 每个 continue 站点必须重置恢复标志
                    # ⚠️ 陷阱：has_attempted_reactive_compact 不在此处重置！
                    #   该标志是跨轮次的持久保护：如果某一轮触发了 reactive compact，
                    #   下一轮不应该再次尝试（防止死循环）。
                    #   该标志只在错误被真正解决后（如上下文确实已缩短）才重置。
                    self.state.consecutive_errors = 0
                    self._emit_turn_end(turn_start)
                    continue  # ← 回到 while True 头部，开始新轮次

                # ── 6. 纯文本响应：触发 Stop Hook 检查 ──
                # LLM 没有请求工具调用，这是"自然停顿"点
                # 运行 Stop Hook 链条判断是否真正终止
                stop_decision = await self._run_stop_hooks(response.text)

                if stop_decision == StopDecision.STOP:
                    self.state.status = AgentState.IDLE
                    yield StateChangeEvent(old=RUNNING, new=IDLE, reason="stop_hook")
                    yield FinalResponseEvent(text=response.text)
                    self._emit_turn_end(turn_start)
                    break  # ← 真正的终止点

                elif stop_decision == StopDecision.EXTRA_TURN:
                    # ★ CONTINUE-SITE-5: Stop Hook 阻塞
                    # Hook 判定需要额外轮次（例如 Hook 追加了系统消息）
                    # ⚠️ 陷阱：不要在 Stop Hook 中做重量级操作（如压缩、网络调用）
                    #   Hook 应该只做逻辑判断，耗时的操作留给下一轮循环
                    self.state.messages = [
                        *self.state.messages,
                        {"role": "user", "content": stop_decision.extra_prompt},
                    ]
                    yield StateChangeEvent(reason="stop_hook_extra_turn")
                    self._emit_turn_end(turn_start)
                    continue  # ← 继续循环

                else:  # CONTINUE
                    # Hook 未决定终止，给 LLM 继续思考的提示
                    self.state.messages = [
                        *self.state.messages,
                        {"role": "user", "content": "Continue your analysis."},
                    ]
                    self._emit_turn_end(turn_start)
                    continue

            # ═══════════════════════════════════════════════
            #  错误恢复：6个恢复性 continue 站点
            # ═══════════════════════════════════════════════
            except PromptTooLongError as e:
                # ★ CONTINUE-SITE-2: Prompt Too Long (HTTP 413)
                # 策略：先尝试 reactive compact（比 proactive compact 更激进）
                #   如果已经尝试过，则升级为 aggressive_snip
                if self.state.has_attempted_reactive_compact:
                    self.context_manager.aggressive_snip(self.state.messages)
                    self.state.has_attempted_reactive_compact = False  # 重置：不同策略
                else:
                    self.context_manager.reactive_compact(self.state.messages)
                    self.state.has_attempted_reactive_compact = True

                self.state.messages = self.context_manager.messages  # 整体替换
                self.state.consecutive_errors += 1
                yield ErrorEvent(type="prompt_too_long", turn=self.state.turn_number,
                                 action="reactive_compact")
                continue

            except MaxOutputTokensError as e:
                # ★ CONTINUE-SITE-3: Max Output Tokens
                # LLM 返回的 finish_reason == "length"，输出被截断
                # 策略：追加 "(continue)" 提示，让 LLM 从截断点续写
                truncated = e.last_message.content
                self.state.messages = [
                    *self.state.messages,
                    {"role": "assistant", "content": truncated},
                    {"role": "user", "content": "Please continue from where you left off."},
                ]
                self.state.consecutive_errors += 1
                yield ErrorEvent(type="max_output_tokens", turn=self.state.turn_number,
                                 action="continue_prompt")
                continue

            except ModelUnavailableError as e:
                # ★ CONTINUE-SITE-4: Fallback Model
                # 主模型不可用（503、超配额、区域限流）
                # 策略：降级到备选模型
                if self.llm_client.has_fallback_model():
                    self.llm_client.switch_to_fallback()
                    yield ErrorEvent(type="model_unavailable",
                                     action="fallback",
                                     from_model=e.primary_model,
                                     to_model=self.llm_client.current_model)
                elif self._should_retry_with_backoff():
                    await asyncio.sleep(self._backoff_delay())
                else:
                    self.state.status = AgentState.ERROR
                    yield StateChangeEvent(old=RUNNING, new=ERROR, reason="model_unavailable")
                    break
                self.state.consecutive_errors += 1
                continue

            except ImageTooLargeError as e:
                # ★ CONTINUE-SITE-6: Image/Media Errors
                # 图片尺寸超出模型限制
                # 策略：移除/压缩问题图片，从消息历史中剥离
                self.context_manager.remove_large_image(e.message_index)
                self.state.messages = self.context_manager.messages  # 整体替换
                self.state.consecutive_errors += 1
                yield ErrorEvent(type="image_too_large", turn=self.state.turn_number,
                                 action="removed_image", detail=e.message_index)
                continue

            except ContextTooLongError as e:
                # ★ CONTINUE-SITE-1: Proactive Compaction 延迟触发
                # 如果前面的 proactive compaction 没拦住，这里做最后的 reactive 压缩
                self.context_manager.emergency_snip(self.state.messages)
                self.state.messages = self.context_manager.messages
                self.state.has_attempted_reactive_compact = True
                self.state.consecutive_errors += 1
                yield ErrorEvent(type="context_too_long", turn=self.state.turn_number,
                                 action="emergency_snip")
                continue

            except RetriableAPIError as e:
                # 通用可重试错误（429、5xx 等）
                if self.state.consecutive_errors >= self.state.max_consecutive_errors:
                    self.state.status = AgentState.ERROR
                    yield StateChangeEvent(old=RUNNING, new=ERROR, reason="max_consecutive_errors")
                    break
                await asyncio.sleep(self._backoff_delay())
                self.state.consecutive_errors += 1
                yield ErrorEvent(type="retriable_api_error", turn=self.state.turn_number)
                continue

            except IrrecoverableError as e:
                # 不可恢复错误（认证失败、账户停用等）
                self.state.status = AgentState.ERROR
                self.state.last_error_type = type(e).__name__
                yield StateChangeEvent(old=RUNNING, new=ERROR, reason=str(e))
                break

    # ═══════════════════════════════════════════════════════════
    #  辅助方法（抽象骨架）
    # ═══════════════════════════════════════════════════════════

    def _emit_turn_end(self, turn_start: float):
        """发出 TurnEndEvent 并重置轮次级标志"""
        elapsed = time.monotonic() - turn_start
        self.event_log.append(TurnEndEvent(turn=self.state.turn_number, duration=elapsed))

    async def _wait_for_resume(self):
        """等待外部 resume 信号——使用 asyncio.Event"""
        ...

    async def _run_stop_hooks(self, response_text: str) -> StopDecision:
        """顺序运行所有 Stop Hook，返回 STOP / EXTRA_TURN / CONTINUE"""
        ...

    def _backoff_delay(self) -> float:
        """指数退避：min(2^consecutive_errors, 60.0) 秒"""
        ...

    def _turn_timeout(self) -> float:
        """计算单轮超时时间（企业级：可以为不同轮次设置不同超时）"""
        ...
```

---

## AI 构建提示

### 7个 Continue 站点深度说明

| # | 站点名称 | 触发条件 | 恢复策略 | 恢复后状态 | 关键陷阱 |
|---|---------|---------|---------|-----------|---------|
| 1 | **Proactive Compaction** | 上下文 token 数超过安全阈值（如 80%） | 调用四级压缩管道，在 LLM 调用前主动缩减消息 | 消息历史被压缩后，同一轮内用压缩后消息重试 | 压缩可能丢失关键上下文；需要保留系统消息和最近的 tool_use 对 |
| 2 | **Prompt Too Long** | LLM API 返回 413（或 Anthropic 的 `prompt_too_long` 错误码） | 先尝试 reactive compaction；若已尝试则升级为 aggressive snip | 整体替换消息历史，hasAttemptedReactiveCompact 置为 True 后重试 | 压缩失败后容易死循环；需要设置 hasAttemptedReactiveCompact 防止无限尝试 |
| 3 | **Max Output Tokens** | LLM 响应的 `stop_reason == "max_tokens"` 或 `finish_reason == "length"` | 在消息历史末尾追加 "(continue)" 提示词 | 同一轮延续对话，让 LLM 从截断点继续 | 如果 LLM 反复触发此站点，最终会耗尽轮次上限 |
| 4 | **Fallback Model** | 主模型返回 503、超配额、或返回模型不可用错误 | 切换到配置的备选模型（如 Claude Haiku → Claude Sonnet） | 模型客户端内部切换后重试 | 备选模型可能有不同的上下文窗口大小和工具支持 |
| 5 | **Stop Hook Blocking** | 至少一个 Stop Hook 返回 `EXTRA_TURN` 决策 | 将 Hook 指定的额外 prompt 追加到消息历史 | 新轮次开始，给 LLM 额外机会响应 | Stop Hook 自身不能执行耗时操作；它只做判断，不做副作用 |
| 6 | **Image/Media Errors** | 发送的图片超过模型尺寸限制（如 Anthropic 的 `image_too_large`） | 从指定索引的消息中移除/压缩问题图片 | 移除图片后的消息历史重试 | 移除图片后语义可能改变；需要通知调用方图片已被剥离 |
| 7 | **Tool Execution** | LLM 返回 `stop_reason == "tool_use"`，要求调用工具 | 执行工具并将结果追加到消息历史 | 新轮次开始，LLM 接收工具结果继续推理 | 这是正常的循环路径，不是"错误"；但需要重置 consecutive_errors 计数器 |

### 恢复策略升级链

```
检测到问题
    │
    ├─→ 站点1: Proactive Compaction (主动，在 LLM 调用前)
    │      │  成功 → 继续
    │      └─→ 失败
    │            │
    ├─→ 站点2: Reactive Compact (被动，413 错误触发)
    │      │  首次 → hasAttemptedReactiveCompact = True
    │      └─→ 再次触发 → aggressive_snip
    │
    ├─→ 站点3: Max Output → 追加 continue prompt
    ├─→ 站点4: Fallback Model → 模型降级
    ├─→ 站点5: Stop Hook → 追加额外轮次
    ├─→ 站点6: Image Error → 移除问题媒体
    └─→ 站点7: Tool Execution → 正常循环
```

### AsyncGenerator 流式模式

Agent 循环不返回最终结果字符串，而是 yield 事件流：

```python
# 调用方代码（伪代码）
async for event in agent.run(user_input="分析这个项目"):
    match event:
        case TurnStartEvent(turn=n):
            print(f"第 {n} 轮开始...")
        case AssistantTextEvent(content=delta, is_final=False):
            print(delta, end="", flush=True)       # 流式打字效果
        case ToolUseEvent(tool_name=name):
            print(f"\n🔧 调用工具: {name}")
        case ToolResultEvent(is_error=True):
            print(f"⚠️ 工具错误")
        case ErrorEvent(action=action):
            print(f"🔄 自动恢复: {action}")
        case FinalResponseEvent(text=result):
            print(f"\n✅ 完成")
```

**设计优势**：
- 每个中间状态独立可观察——调用方知道 Agent 在干什么
- 错误恢复过程透明——调用方可以看到何时触发 compact、何时切换模型
- 实时 UI 更新——支持流式打字效果、进度条、工具调用动画

---

## 会话事件日志设计

### 设计原则

**类比数据库 WAL (Write-Ahead Log)**：事件必须先写入持久化存储（WAL），然后才能 yield 给调用方。这保证了即使进程崩溃，会话历史也可以从日志文件中完整重建。

### 5种事件类型

| 事件类型 | 触发时机 | 必填字段 | 示例 |
|---------|---------|---------|------|
| `user_message` | 用户发送新的输入 | `content` | `{"type":"user_message","content":"分析这个项目"}` |
| `assistant_text` | LLM 返回文本（流式块或最终块） | `content`, `is_final` | `{"type":"assistant_text","content":"Hello","is_final":false}` |
| `tool_use` | LLM 请求调用工具 | `tool_name`, `tool_input`, `tool_use_id` | `{"type":"tool_use","tool_name":"read_file","tool_input":{"path":"a.txt"},"tool_use_id":"tool_001"}` |
| `tool_result` | 工具执行返回结果 | `tool_use_id`, `content`, `is_error` | `{"type":"tool_result","tool_use_id":"tool_001","content":"...","is_error":false}` |
| `turn_start` / `turn_end` | 每轮开始/结束 | `turn_number`, `timestamp` | `{"type":"turn_start","turn_number":3,"timestamp":1716220800.123}` |

### JSONL 格式规范

```
# 文件路径: memory/sessions/{session_id}.jsonl
# 每行一条完整的 JSON 记录，不换行
# append-only：只追加，从不修改或删除

{"type":"turn_start","turn_number":1,"ts":1716220800.123}
{"type":"user_message","content":"分析这个项目","ts":1716220800.150}
{"type":"assistant_text","content":"我来分析...","is_final":false,"ts":1716220801.200}
{"type":"tool_use","tool_name":"read_file","tool_input":{"path":"src/main.py"},"tool_use_id":"tool_001","ts":1716220801.500}
{"type":"tool_result","tool_use_id":"tool_001","content":"import...","is_error":false,"ts":1716220802.100}
{"type":"assistant_text","content":"文件内容显示...","is_final":true,"ts":1716220803.000}
{"type":"turn_end","turn_number":1,"duration":2.9,"ts":1716220803.010}
```

### 不可变性与回放

```python
class SessionEventLog:
    """
    会话事件日志 —— 追加不可变日志。

    设计约束:
      - __init__ 时创建或打开 .jsonl 文件句柄
      - append(event) → 先写入文件、再追加到内存列表、再 yield 事件
      - 没有 delete / update / truncate 操作
      - 支持 replay(session_id) → 重放所有事件以重建 AgentState

    回放算法（伪代码）:
      for line in open(f"{session_id}.jsonl"):
          event = json.loads(line)
          match event.type:
              case "user_message" | "assistant_text":
                  state.messages.append({"role": ..., "content": event.content})
              case "tool_use":
                  pending_tool_uses.add(event.tool_use_id)
              case "tool_result":
                  state.messages.append({"role": "user", "content": event.content})
              case "turn_end":
                  state.turn_number = event.turn_number
    """
```

---

## 规模适应性指南

### Minimal（演示/原型 ~50 行核心逻辑）

```
特征:
  - 简单 while True 循环
  - 一个 broad except Exception 捕获所有错误
  - 无重试：catch → 记录日志 → break
  - 无状态机（只区分"运行中"和"已终止"）
  - 无流式输出（async def run() -> str）
  - 无会话日志

适用场景: 一次性脚本、本地测试、快速原型

伪代码骨架:
  while True:
      try:
          response = await llm.chat(messages, tools)
          if response.has_tool_uses:
              results = execute_tools(response.tool_uses)
              messages.extend(format(results))
              continue
          return response.text
      except Exception:
          break
```

### Professional（生产可用 ~300 行核心逻辑）

```
特征:
  - 完整 7 个 continue 站点
  - 状态机：idle / running / expired / error（无 paused）
  - 指数退避重试（consecutive_errors 计数器 + max_consecutive_errors 上限）
  - 轮次上限 + 单级超时
  - 半流式：yield TurnStart/TurnEnd/Error 事件，文本块做简单的 yield
  - SessionEventLog 写入本地 .jsonl
  - hasAttemptedReactiveCompact 标志（注意重置时机）

适用场景: 内部工具、CLI 应用、辅助开发

关键添加强化点:
  - 将 "metadata" 或 "__system__" 消息适配到各提供商的 API 格式
  - 工具调用并行化（并发安全工具同时执行）
  - consecutive_errors 计数器在站点7（正常工具完成）处重置
```

### Enterprise（高可用系统 需要集成基础设施）

```
特征:
  - AsyncGenerator 完整流式模式：每个内部事件都 yield
  - 双重超时：turn_level_timeout + session_level_timeout
  - 完整的五状态机含 PAUSED（支持暂停/续跑/迁移）
  - 会话回放：从 .jsonl 重建完整 AgentState
  - 模型降级链：primary → fallback1 → fallback2
  - 错误事件聚合到监控系统（Prometheus / Datadog 指标）
  - 分布式会话：Redis 存储状态 + S3 存储事件日志
  - 消息去重：tool_use_id 去重防止重试时重复执行副作用工具

适用场景: 面向客户的产品、高可用服务、需要审计追踪的系统

企业级额外约束:
  - WAL-before-yield 保证：事件先 fsync 再 yield
  - 会话迁移：序列化 AgentRunState → 另一进程恢复
  - 熔断器：如果 same_error 连续出现 N 次，主动 expire
  - Canary 发布：新模型先作为 fallback，逐步提升为 primary
```

---

## 检查清单

- [ ] 主循环是真正的 `while True`，不会在首次文本响应时退出
- [ ] 7个 continue 站点全部有专属的错误类型匹配（不是通用的 `except Exception`）
- [ ] `has_attempted_reactive_compact` 在站点2触发前检查，防止 dead loop
- [ ] `consecutive_errors` 在站点7（正常工具执行）后重置为 0
- [ ] 状态机状态转换合法（idle→running→{idle|expired|error}，running→paused→running）
- [ ] 会话超时使用 `time.monotonic()` 而非 `time.time()`（不受系统时钟调整影响）
- [ ] 流式响应时 `assistant_text` 块正确累积（不能丢失，不能重复）
- [ ] 工具结果以"整体替换"语义追加到 `state.messages`（不原地修改）
- [ ] Stop Hook 内部不执行网络调用、文件 I/O、或其他重量操作
- [ ] SessionEventLog 是 append-only，事件先写盘再 yield
- [ ] 轮次上限和会话级超时都作为 break 条件检查
- [ ] 备选模型（fallback）有匹配的上下文窗口和工具支持

---

## 常见陷阱

### 陷阱1：`hasAttemptedReactiveCompact` 不重置

```python
# ❌ 错误：在 while 循环顶部重置标志
self.state.has_attempted_reactive_compact = False  # 每轮都重置 → 可能死循环

# 正确：该标志是跨轮次的持久保护
#    - 在站点2（Prompt Too Long）触发时设置 True
#    - 仅在 aggressive_snip 成功后重置 False（因为我们用了不同的策略）
#    - 不在普通循环点重置 —— 它的存在意义就是"防止同一错误反复触发同样的恢复"
```

### 陷阱2：在 Stop Hook 中执行重量操作

```python
# ❌ 错误：Stop Hook 中执行网络调用
class AuditStopHook:
    async def check(self, response_text: str) -> StopDecision:
        audit_result = await self.audit_api.check(response_text)  # 网络调用！
        if audit_result.needs_revision:
            return StopDecision.EXTRA_TURN
        return StopDecision.STOP

# ✅ 正确：Hook 只做逻辑判断，副作用留给下一轮
class AuditStopHook:
    async def check(self, response_text: str) -> StopDecision:
        # 只写一个"待审计"标记到消息历史
        # 网络调用在下一轮由专门的 tool 执行
        if self._has_sensitive_pattern(response_text):
            return StopDecision.EXTRA_TURN(prompt="请审计上一轮的输出")
        return StopDecision.STOP
```

### 陷阱3：流式块丢失——累积逻辑错误

```python
# ❌ 错误：只 yield 不累积
async for chunk in llm.stream(messages):
    yield AssistantTextEvent(content=chunk.delta)  # 流式 OK
# 但完整的 response.text 无法从 chunks 重建！

# ✅ 正确：同时累积和 yield
accumulated = []
async for chunk in llm.stream(messages):
    accumulated.append(chunk.delta)
    yield AssistantTextEvent(content=chunk.delta)
response.text = "".join(accumulated)  # 完整文本用于后续处理
```

### 陷阱4：状态原地修改导致回滚困难

```python
# ❌ 错误
self.state.messages.append({"role": "user", "content": tool_result})

# ✅ 正确：整体替换（伪不可变语义）
self.state.messages = [*self.state.messages, {"role": "user", "content": tool_result}]
```

### 陷阱5：忘记检查暂停信号

在 while 循环中的多个 continue 站点之间，如果 Agent 执行了预先插件化的工作流（如 MCP 工具链），可能花费数分钟。在此期间外部可能已经发送了 pause 信号。解决：在长耗时操作之前/之后主动检查 `self.state.pause_requested`。

---

## 下一步

完成 Phase 4 后，进入 **Phase 5: 上下文管理**（参考 `references/05-phase-context.md`），实现四级压缩管道来确保上下文不会被耗尽。