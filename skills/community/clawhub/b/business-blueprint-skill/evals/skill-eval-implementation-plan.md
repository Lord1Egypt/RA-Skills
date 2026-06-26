# Business Blueprint Skill Eval Implementation Plan

Date: 2026-05-17

Scope: `kai-business-blueprint` / `business-blueprint-skill`

Release: `v0.16.2`

Initial eval release: `v0.16.1`

## 背景

本次改动的目标是给 `business-blueprint-skill` 建立 OpenAI-style skill eval，而不是给 `report-creator` 做 eval。`report-creator` 已经有自己的 eval；本方案专门覆盖业务蓝图 skill 的触发、流程、产物质量和效率。

核心问题：

- 过去已有导出/回归测试，但缺少「一次 skill 运行」层面的评分。
- 需要现在建立可保存、可比较的基线分数，后续 skill 修改才能判断是否退化。
- eval 不能依赖 Codex、Claude、Qoder、OpenClaw 或任何 live agent 环境。

## 成功标准

本次方案以以下条件作为完成标准：

- 默认 eval 可离线运行。
- 默认 eval 不调用任何 agent、模型 API 或网络。
- eval 输入是 agent-agnostic normalized trace，不绑定某个 CLI 的事件格式。
- 每个 case 都产生四类分数：Outcome、Process、Style、Efficiency。
- 基线分数保存到仓库，后续改动可以直接比较。
- release verification 默认包含 fixture skill eval。
- README 中英文和 eval 文档都写明运行方式和边界。

## 架构决策

### 1. 使用 normalized trace 作为唯一稳定接口

eval harness 不解析 Codex/Claude/Qoder 的原始事件。外部真实运行如果要评分，必须先转换成统一的 `normalized-v1` JSON。

最小 trace contract：

```json
{
  "runner": "fixture",
  "trace_format_version": "normalized-v1",
  "tool_calls": [],
  "shell_commands": [],
  "failed_shell_commands": [],
  "read_paths": [],
  "write_paths": [],
  "artifact_paths": [],
  "input_tokens": null,
  "output_tokens": null,
  "wall_ms": 0,
  "run_completed": true,
  "skill_evidence": {
    "skill_contract_read": false,
    "blueprint_flow_observed": false,
    "validate_observed": false,
    "export_observed": false,
    "projection_observed": false
  },
  "runner_warnings": []
}
```

默认 runner：

- `fixture`：读取仓库内 fixture trace，用于 CI/release verification/baseline。
- `trace`：读取外部传入的 normalized trace，用于人工比较任意 agent 的真实运行结果。

刻意不提供：

- `codex` runner
- `claude` runner
- `qoder` runner
- `--run-live`
- raw trace parser

原因：这些都会把 eval 绑定到某个 agent 环境或事件格式，破坏可移植性。

### 2. 四类评分，每类 25 分

每个 case 总分 100：

| Category | Weight | 关注点 |
| --- | ---: | --- |
| Outcome | 25 | 是否生成了正确蓝图、projection、SVG/HTML 等目标产物 |
| Process | 25 | 是否读了 skill contract 和必要 reference，是否走了 validate/export/project 流程 |
| Style | 25 | 行业、蓝图类型、语义密度、占位符、rubric 质量 |
| Efficiency | 25 | shell 命令数、失败重试、token、wall time 是否在预算内 |

硬门槛：

- positive case 没有 `.blueprint.json` 直接失败，不能靠其他分数补回来。
- negative case 生成蓝图/导出产物直接失败。
- incomplete trace 不能通过。
- 缺少 style rubric 时标记 `eval_complete=false`，避免把未完成的评估当成通过。

## Case 设计

Prompt manifest: `evals/blueprint-skill-prompts.csv`

| Case | Kind | Should Trigger | 目标 |
| --- | --- | --- | --- |
| `explicit-blueprint` | explicit | true | 明确要求使用 business blueprint skill，生成 retail 架构蓝图 + SVG/HTML |
| `implicit-meeting-notes` | implicit | true | 中文会议纪要隐式触发制造业蓝图 |
| `contextual-domain-knowledge` | contextual | true | domain-knowledge 蓝图路径，覆盖知识治理实体 |
| `boundary-projection-handoff` | boundary | true | 生成 finance 蓝图和 projection，但不越界生成下游 report/slide |
| `negative-report` | negative | false | 老板周报应转交 report 类 skill，不应生成业务蓝图 |
| `negative-slide-deck` | negative | false | PPT 请求应转交 slide/presentation 类 skill，不应生成业务蓝图 |

## 文件结构

新增核心文件：

- `scripts/run-skill-evals.py`：agent-agnostic eval harness。
- `scripts/verify-release.py`：release verification 入口，默认跑 pytest + fixture skill eval。
- `evals/blueprint-skill-prompts.csv`：case manifest。
- `evals/skill-prompts/*.md`：prompt fixtures。
- `evals/skill-run-rubric.schema.json`：style rubric schema。
- `scripts/tests/fixtures/skill-evals/*.json`：normalized trace fixtures 和 style rubric fixtures。
- `scripts/tests/fixtures/skill-evals/artifacts/*`：fixture artifacts。
- `evals/baselines/2026-05-17-skill-evals-fixture.json`：当前基线结果。
- `evals/baselines/2026-05-17-baseline-summary.md`：人类可读基线摘要。

同时更新：

- `README.md`
- `README.zh-CN.md`
- `evals/README.md`
- `SKILL.md`

## 当前基线

命令：

```bash
python3 scripts/run-skill-evals.py --root . --runner fixture --format json --json-out evals/baselines/2026-05-17-skill-evals-fixture.json
```

汇总：

| Metric | Value |
| --- | ---: |
| Cases | 6 |
| Passed | 6 |
| Failed | 0 |
| Incomplete | 0 |
| Average score | 99.67 |
| Outcome average | 25.00 |
| Process average | 25.00 |
| Style average | 24.67 |
| Efficiency average | 25.00 |

Case 分数：

| Case | Score | Outcome | Process | Style | Efficiency |
| --- | ---: | ---: | ---: | ---: | ---: |
| `explicit-blueprint` | 100 | 25 | 25 | 25 | 25 |
| `implicit-meeting-notes` | 99 | 25 | 25 | 24 | 25 |
| `contextual-domain-knowledge` | 100 | 25 | 25 | 25 | 25 |
| `boundary-projection-handoff` | 99 | 25 | 25 | 24 | 25 |
| `negative-report` | 100 | 25 | 25 | 25 | 25 |
| `negative-slide-deck` | 100 | 25 | 25 | 25 | 25 |

## 运行方式

默认离线基线：

```bash
python3 scripts/run-skill-evals.py --root . --runner fixture
```

发布验证：

```bash
python3 scripts/verify-release.py --root .
```

外部运行结果评分：

```bash
python3 scripts/run-skill-evals.py \
  --root . \
  --runner trace \
  --case-id <case-id> \
  --normalized-trace <trace.json>
```

外部 trace 必须已经转换成 normalized schema。这个仓库不负责启动 live agent。

## 验证结果

本次发布前验证：

```text
python3 -m pytest scripts/tests -q
274 passed, 1 skipped

python3 scripts/run-skill-evals.py --root . --runner fixture
6 passed, 0 failed, 0 incomplete; average score 99.67/100

python3 scripts/verify-release.py --root . --format json
2 passed, 0 failed
```

## 发布信息

GitHub Release:

- <https://github.com/kaisersong/kai-business-blueprint/releases/tag/v0.16.2>

Direct zip:

- <https://github.com/kaisersong/kai-business-blueprint/releases/download/v0.16.2/kai-business-blueprint-v0.16.2.zip>

ClawHub:

- `business-blueprint-skill@0.16.2`

## 后续扩展规则

添加新 case 时：

1. 在 `evals/blueprint-skill-prompts.csv` 增加 manifest 行。
2. 在 `evals/skill-prompts/` 增加 prompt。
3. 在 `scripts/tests/fixtures/skill-evals/` 增加 normalized trace fixture。
4. positive case 增加对应 artifact fixture 和 style rubric。
5. 重新运行 fixture baseline，并更新 `evals/baselines/`。

添加外部 agent 支持时：

- 不要在 harness 里添加 live runner。
- 不要把 raw event parser 变成默认 release 路径。
- 先在外部工具中把真实运行转换为 normalized trace。
- 只把 normalized trace 交给 `--runner trace` 评分。
