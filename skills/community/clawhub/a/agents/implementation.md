# Implementation — The Patterns As Code

Runnable shapes for the rules in SKILL.md. Written in the language `language` selects; the samples below are Python, and the TypeScript differences are at the end. Framework-specific equivalents are in `frameworks.md`.

**Contents:** [The loop with all three caps](#the-loop-with-all-three-caps) · [Tool executor](#tool-executor-tiers-idempotency-actionable-failures) · [Loop detection](#loop-detection) · [Retries](#retries-with-jitter-and-a-budget) · [Compaction](#compaction-that-preserves-what-matters) · [Checkpoints](#checkpoints-and-resume) · [Parallel tools](#parallel-tool-calls) · [Structured decisions](#structured-decisions) · [Tracing](#tracing-a-turn) · [TypeScript](#typescript-differences)

## The Loop With All Three Caps

The reference implementation of SKILL.md Rules 2 and 9. Note the end reason: it is the field every later diagnosis starts from.

```python
from dataclasses import dataclass, field
from time import monotonic

@dataclass
class Run:
    reason: str = "running"       # done | max_turns | budget | timeout | error | escalated
    turns: int = 0
    spend_usd: float = 0.0
    result: str | None = None

def run_agent(messages, tools, cfg) -> Run:
    run, started = Run(), monotonic()
    while True:
        if run.turns >= cfg.max_turns:                 run.reason = "max_turns"; break
        if run.spend_usd >= cfg.cost_ceiling_per_task_usd: run.reason = "budget"; break
        if monotonic() - started >= cfg.deadline_s:    run.reason = "timeout"; break

        reply = model(messages, tools=tools, timeout=cfg.turn_timeout_s)
        run.turns += 1
        run.spend_usd += price(reply.usage)            # count BEFORE the next turn, not after the loop

        if not reply.tool_calls:
            run.reason, run.result = "done", reply.text
            break
        messages += [reply] + execute_all(reply.tool_calls, cfg)
    return run
```

- Count spend inside the loop. A budget checked only at the end is a report, not a cap.
- A cap that trips returns the partial result and the reason to the caller, so it can resume from a checkpoint instead of restarting (→ Checkpoints).
- `turn_timeout_s` is separate from `deadline_s`: one bounds a single call, the other the whole task.

## Tool Executor: Tiers, Idempotency, Actionable Failures

Enforcement lives here, not in the prompt (SKILL.md Rules 4, 5, 6).

```python
TIERS = {"read": 0, "write": 1, "external": 2, "irreversible": 3}
ALLOWED = {"suggest": 0, "approve-writes": 0, "autonomous": 2}   # ceiling per autonomy_level

def execute(call, cfg, task_id):
    spec = TOOLS.get(call.name)
    if spec is None:
        return fail(call, f"unknown tool '{call.name}'. Available: {', '.join(TOOLS)}")

    tier = TIERS[spec.tier]                                   # undeclared tier -> irreversible upstream
    if tier > ALLOWED[cfg.autonomy_level]:
        decision = request_approval(call, spec)               # human-in-the-loop.md
        if not decision.granted:
            return fail(call, f"not approved: {decision.reason}. Do not retry; propose an alternative.")

    if spec.tier in ("write", "external", "irreversible"):
        key = f"{task_id}:{call.name}:{stable_hash(call.args)}"
        if (prior := ledger.get(key)) is not None:
            return ok(call, prior, already_done=True)
        ledger.reserve(key)                                   # BEFORE the side effect, not after

    try:
        result = spec.fn(**call.args)
    except ValidationError as e:
        return fail(call, f"{e.field} is invalid: {e.message}. Fix that argument and call again.")
    except UpstreamTimeout:
        return fail(call, "upstream timed out. Retry once; if it fails again, tell the user and stop.")
    except Unauthorized:
        return fail(call, "not authorized for this resource. Do not retry. Escalate.")

    result = truncate(result, max_tokens=cfg.max_tool_result_tokens)   # tools.md
    ledger.commit(key, result) if spec.tier != "read" else None
    return ok(call, result)
```

Every `fail` carries what broke, which argument, and what to do next. That third clause is what stops identical retries.

## Loop Detection

```python
def is_stuck(history, window=3):
    recent = [(c.name, stable_hash(c.args)) for c in history[-window:]]
    return len(recent) == window and len(set(recent)) == 1
```

On a hit, do not just break: inject an observation the model can act on — `"You have called lookup_order with the same arguments 3 times and the result has not changed. Try a different tool or ask the user."` A silent break turns a diagnosable loop into a mysterious truncation.

## Retries With Jitter And A Budget

```python
def with_retries(fn, budget=3, base=0.5, cap=8.0):
    for attempt in range(budget):
        try:
            return fn()
        except Retryable as e:
            if attempt == budget - 1:
                raise
            sleep(min(cap, base * 2 ** attempt) * (0.5 + random()))   # full-ish jitter
```

- The retry budget belongs to the **task**, not to each call site: three retries in each of four tools is twelve extra calls and four times the latency.
- Never retry a non-idempotent external call without the ledger check above.
- Retries are the usual cause of a p95 latency that is many times the median (`production.md`).

## Compaction That Preserves What Matters

```python
PRESERVE = ("goal", "constraints", "plan", "decisions", "committed_effects")

def compact(messages, state, keep_last=6):
    head, middle, tail = messages[:1], messages[1:-keep_last], messages[-keep_last:]
    summary = model(SUMMARIZE_PROMPT + render(middle)).text
    state["compactions"] = state.get("compactions", 0) + 1
    return head + [system(render_state(state, PRESERVE)), system(summary)] + tail
```

- The state block is re-emitted verbatim; only the middle is summarized (`context.md`).
- Trigger at ~70-80% of the window, never at overflow — the summarizing call needs room too.
- Track `compactions`; at three, checkpoint and start a fresh context from the checkpoint rather than summarizing a summary.

## Checkpoints And Resume

```python
def checkpoint(task_id, state):
    store.put(task_id, {"goal": state["goal"], "step": state["step"],
                        "done_steps": state["done_steps"],
                        "committed_effects": state["committed_effects"],
                        "ts": now()})

def resume(task_id):
    return store.get(task_id)     # None -> fresh run
```

Checkpoint immediately after every irreversible action, before anything else. The failure you cannot afford is repeating a payment because the process died between the charge and the log.

## Parallel Tool Calls

```python
async def execute_all(calls, cfg):
    reads  = [c for c in calls if TOOLS[c.name].tier == "read"]
    writes = [c for c in calls if TOOLS[c.name].tier != "read"]
    sem = asyncio.Semaphore(cfg.max_parallel_tools)            # 5 is a sane ceiling

    async def guarded(c):
        async with sem:
            return await run_in_executor(execute, c, cfg)

    results = await asyncio.gather(*(guarded(c) for c in reads), return_exceptions=True)
    results = [r if not isinstance(r, Exception) else fail(c, str(r)) for c, r in zip(reads, results)]
    for c in writes:                                            # serialized on purpose
        results.append(execute(c, cfg))
    return results
```

Return one result per call, never one aggregated error: the model can act on "3 of 5 succeeded".

## Structured Decisions

```python
class Decision(BaseModel):
    reasoning: str
    action: Literal["search", "write", "ask_user", "escalate", "done"]
    arguments: dict
    confidence: float           # only useful if it is calibrated against your eval set
```

Structured output makes routing testable and the trajectory scoreable (`evaluation.md`). Treat `confidence` as a signal to *measure*, not to trust: check whether low-confidence runs actually fail more often before you gate anything on it.

## Tracing A Turn

```python
span = {
    "task_id": task_id, "turn": run.turns,
    "tool": call.name, "args_hash": stable_hash(call.args),
    "result_bytes": len(result), "latency_ms": ms,
    "tokens_in": u.input, "tokens_out": u.output, "cached_in": u.cache_read,
    "model": cfg.model_snapshot, "prompt_version": cfg.prompt_version,
    "end_reason": run.reason,
}
```

`model`, `prompt_version` and `end_reason` are what make a trace answerable weeks later — they are also the three fields most often missing (`debugging.md`).

## TypeScript Differences

- `asyncio.gather` → `Promise.allSettled`, which already gives you per-call results instead of one rejection.
- Concurrency limiting has no standard primitive: a small semaphore or a pool library, and cap it explicitly.
- Structured output: a schema validator (Zod-style) at the tool boundary, both for arguments in and results out.
- Timeouts need an `AbortController` per call; a promise with no abort keeps running and keeps costing after you stopped waiting for it.
- Monetary and token counters belong in a single mutable run object, as above — closure-captured counters silently diverge across retries.

**When a loop, executor or checkpoint shape is settled for a project**, save it to `~/Clawic/data/agents/artifacts/<kebab-name>.md` with the reasoning behind each cap and its `## Boxes` line, in the same turn (`memory-template.md`). The caps are the part that gets loosened during an incident and never restored.
