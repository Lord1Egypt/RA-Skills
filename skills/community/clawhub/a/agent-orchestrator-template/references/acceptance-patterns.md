# Acceptance Patterns

Acceptance is where orchestration becomes reliable. A sub-agent reporting "done" is not completion.

The main agent must verify:

1. task boundary compliance
2. workflow compliance
3. output completeness
4. verification evidence
5. cross-agent consistency

## Acceptance Checklist

Before claiming completion, check:

- [ ] Was the correct task type chosen?
- [ ] Did the sub-agent stay inside the owned scope?
- [ ] Did it avoid forbidden files or forbidden actions?
- [ ] Did it produce the expected output artifact?
- [ ] Is the work materially complete?
- [ ] Was the claimed verification actually run?
- [ ] Does the result conflict with any other agent output?
- [ ] Does the user need synthesis instead of raw fragments?

## Boundary Compliance

The most common failure in multi-agent work is scope drift.

Verify:

- the agent touched only its owned files or owned scope
- the agent did not modify blocked or reserved areas
- the output matches the contract goal
- the agent did not silently expand the task

If a sub-agent exceeded scope, do not accept the result without review, even if the result looks useful.

## Verification Standards By Task Type

| Task Type | Minimum Acceptance Criteria |
|-----------|----------------------------|
| `explore` | Findings are relevant, bounded, and traceable to inspected sources |
| `implement` | Changes stay in scope, target behavior is implemented, required checks are run |
| `verify` | Review criteria are explicit, evidence is shown, unresolved risk is named |
| `operate` | Requested side effect occurred, target path/system is correct, failures are explicit |

## Cross-Agent Conflict Check

When multiple agents contribute, verify:

- outputs do not contradict each other
- file ownership did not overlap unexpectedly
- one agent did not invalidate another's result
- synthesis reflects the final integrated state

If two outputs conflict, the main agent must resolve the conflict before presenting the result.

## Synthesis Rules

Always synthesize when:

- multiple agents contributed to one user-facing result
- raw outputs contain internal notes, session IDs, or fragments
- one result depends on interpretation of another

Forward as-is only when:

- one agent produced a clean, user-ready artifact
- no internal metadata leaks through
- no integration step is needed

## Exception Patterns

### Sub-Agent Blocked

When a sub-agent is blocked:

1. Identify the exact blocking step
2. Decide whether the main agent can finish the missing part
3. Re-route only if another agent has a better fit
4. Update routing rules if the failure was systematic

### Scope Violation

When a sub-agent exceeded its boundary:

1. mark result as `needs_review`
2. inspect all changed scope
3. keep safe portions if useful
4. reject or repair the overreach
5. tighten future task contracts

### False Completion

When a sub-agent claims completion without evidence:

1. do not repeat the claim
2. run or inspect the required verification directly
3. report actual status
4. tighten the acceptance checklist for that task class

## Exception Reporting Template

Use this when delegated work fails or needs escalation:

```text
任务: [original task description]
任务类型: [explore / implement / verify / operate]
领域: [code / knowledge / content / ...]
预期输出: [artifact or result]
拥有范围: [files or scope]
禁止范围: [files or scope]
当前状态: [blocked / needs_review / abandoned]
卡在哪一步: [specific step or tool]
验证证据: [present / missing]
补救建议: [local fix / reroute / ask user]
```

## Delivery Templates

### Code Task

```text
任务: [feature or bug]
任务类型: implement
执行 agent: [worker id]
拥有范围: [file paths]

验收结果:
- [x] 修改范围符合任务契约
- [x] 目标行为已覆盖
- [x] 验证命令已运行
- [ ] 仍有风险: [if any]

主 agent 结论:
[accept / repair / reroute]
```

### Knowledge Task

```text
任务: [archive or note task]
任务类型: operate
执行 agent: [worker id]
目标路径: [knowledge path]

验收结果:
- [x] 已写入正确路径
- [x] 非 daily memory
- [x] 去重已检查
- [x] 资源文件已处理

主 agent 结论:
[accept / repair / reroute]
```

### Verification Task

```text
任务: [review target]
任务类型: verify
执行 agent: [reviewer or main]

验收结果:
- [x] 评审标准明确
- [x] 证据已列出
- [x] 剩余风险已注明

主 agent 结论:
[accept / continue / escalate]
```

## Common Pitfalls

| Pitfall | How To Avoid |
|---------|--------------|
| Accepting "done" without evidence | Require direct verification or inspect evidence |
| Letting workers edit outside scope | Define owned and forbidden scope in every task contract |
| Parallel workers colliding on files | Check write-set overlap before dispatch |
| Forwarding raw fragments to the user | Synthesize after review |
| Misclassifying a blocking task as delegable | Keep critical-path work local |
