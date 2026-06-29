# Checker And Evidence Gate

## 中文

本 reference 用于 CMS Lite / Agent Loop Engineering 的验证门禁。核心原则：

> checker 只能证明 loop 状态文件结构可信，不能单独证明产品功能已经正确。

因此：

- `agent-loop-check.ps1` 的 `Done` 表示 `Docs/` 状态合法。
- 真正的完成还需要项目验证证据，例如测试、类型检查、构建、功能检查、截图、日志或人工验收。
- Agent 不能只写“测试通过”；必须记录运行了什么命令、结果是什么、关键证据在哪里。
- `Done` 必须至少有一个自动验证证据和一个功能验证证据。

## CMS Lite v0.2 Evidence Fields

在测试阶段，`Docs/LOOP_LOG.jsonl` 应记录可机器读取的验证结果：

```json
{
  "timestamp": "2026-06-10T00:00:00Z",
  "event": "loop_end",
  "scenario_guess": "Small",
  "skill_used": "agent-loop-engineering",
  "checker_result": "Done",
  "verified_at": "2026-06-10T00:00:00Z",
  "verification_commands": [
    {
      "kind": "automatic",
      "command": "pytest",
      "exit_code": 0,
      "summary": "3 passed"
    },
    {
      "kind": "functional",
      "command": "python app.py --demo",
      "exit_code": 0,
      "summary": "CLI returned expected JSON"
    }
  ]
}
```

Allowed `kind` values:

- `automatic`: test, typecheck, build, lint, static check, unit test, integration test.
- `functional`: UI check, CLI check, API call, screenshot comparison, user-flow check, manual acceptance evidence.
- `other`: supporting evidence that is not enough for `Done` by itself.

## Strict Mode

Use checker strict mode when evaluating a completion claim:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\agent-loop-check.ps1 -WorkspacePath "D:\path\to\project" -Strict
```

Strict mode should fail `Done` when:

- no successful verification command is recorded in `LOOP_LOG.jsonl`;
- no successful automatic evidence is recorded;
- no successful functional evidence is recorded;
- `verified_at` is missing from the record or verification command;
- `LOOP_STATE.md` says `Done` but `LOOP_LOG.jsonl` has no matching completion evidence.

Strict mode still does not judge code quality, UI beauty, architecture quality, or whether a human is satisfied. Those require project-specific tests, screenshots, review, or human confirmation.

## Cross-Repo Checker Use

The checker can be kept in one skill or test-suite folder and pointed at any repository that contains `Docs/`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "D:\Codex\clawhub-skills\ClawSkills\skills\agent-loop-engineering\scripts\agent-loop-check.ps1" -WorkspacePath "D:\Development\SomeProject" -Strict -Json
```

Use a real path. Do not paste placeholder brackets such as `<project-path>` into PowerShell.

## Expanded Docs Health Check

For expanded/full Agent Loop projects that use `WORK_ORDER.md`, `ACCEPTANCE.md`,
and `LOOP_RUNS.jsonl`, run the read-only health checker during Controller review
or before archive:

```powershell
node .\scripts\agent-loop-health-check.mjs --workspace "D:\path\to\project"
```

The checker reports:

- duplicate acceptance IDs in Markdown table rows;
- raw loop feedback pasted into `ACCEPTANCE.md`;
- environment-sensitive `WORK_ORDER.md` files that do not name local/cloud mode,
  provider/config, feature flags, waived conditions, or mandatory validation;
- invalid `LOOP_RUNS.jsonl` records;
- obvious contradictions such as latest status `Done` with failed validation.

It is deliberately read-only. Treat checker errors as `Invalid State` and have
the project's Controller or maintainer clean up the state; do not let the
checker auto-edit project files.

## English

This reference defines the evidence gate for CMS Lite / Agent Loop Engineering.

The checker validates the loop state protocol. It does not prove that the product is correct by itself.

Rules:

- `agent-loop-check.ps1` returning `Done` means the local `Docs/` state is valid.
- Product completion still needs project verification evidence.
- Agents must record the actual verification commands, exit codes, short results, and evidence locations.
- `Done` requires at least automatic evidence plus functional evidence.
- Use `-Strict` before accepting a completion claim.
- For expanded `Docs/` projects, use `agent-loop-health-check.mjs` to catch
  duplicate acceptance rows, missing work-order environment notes, JSONL issues,
  and obvious Done/evidence contradictions.
