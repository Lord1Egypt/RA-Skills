# code-refactor

An agent skill that restructures, rewrites, or ports existing code to another language **while proving behavior is preserved** — with characterization tests, parity fixtures and staged, verifiable steps instead of big-bang changes.

一个 Agent 技能：重构、重写或把现有代码移植到另一种语言，并用特征测试、对拍样例和分步验证**证明行为不变**。

## Modes / 模式

| Mode | When | How behavior is proven |
|---|---|---|
| **refactor** | Same language, the structure is the problem: split a god module into a package, untangle circular imports, move modules, change a signature across all callers, migrate an internal API step by step | Existing code survives and moves in small mechanical steps; tests stay green between steps |
| **rewrite** | Same language, the code isn't worth evolving: unreadable legacy, a dead framework, "rewrite from scratch" | The old implementation becomes the oracle: characterization tests first, then a parity check old vs new |
| **port** | The target language differs (Python → Go/Rust, TS → Go/Rust, Java → Kotlin, C → Rust, …) | Shared fixtures and a modest differential run against both implementations; numeric, string, error, ordering and concurrency semantics are mapped explicitly |

Guardrails / 硬性规则: the skill is read before searching files (even in an empty workspace); it stays inside the working directory, never installs toolchains without approval, writes no files for plan-only requests, works to a time/step budget (smallest verifiable slice first, report written early), and finishes instead of leaving a resume note.

Prefer refactor over rewrite whenever an incremental path exists. "Port and clean it up" is two projects: port first, refactor later. For tidying a single function or snippet, use [simplify-code](https://github.com/linkxzhou/simplify-code).

## Language pairs / 语言对

Mapping tables in `references/port-pairs.md`:

- Python ↔ Go · Python ↔ Rust
- JavaScript/TypeScript → Rust · Rust → TypeScript
- TypeScript ↔ Go
- Java ↔ Kotlin
- C → Rust · Rust → C (FFI surface)
- JavaScript → TypeScript (gradual typing)

Other pairs follow the general playbook in `references/port-playbook.md`.

## Install / 安装

```bash
npx skills add linkxzhou/code-refactor
```

Or clone it into your skills folder:

```bash
git clone --depth 1 https://github.com/linkxzhou/code-refactor.git ~/.claude/skills/code-refactor
```

## Structure / 结构

```
SKILL.md        # Skill definition: mode choice, safety gates, step-by-step workflows, report format
references/     # Port pairs, port playbook, refactoring catalog, rewrite checklist, safety net, templates, sources
evals/          # Eval cases, trigger evals and fixtures
```

## Evals / 评测

Agent model `glm-5.3-flash-external` via miniagent, 2026-10-19. 8 cases covering all three modes: Python module split, callback→async plan, legacy JS rewrite, and ports Python→Go, Java→Kotlin, C→Rust, Python→Rust and TS→Go. Assertions are behavior-focused and graded by hand. One run per case, with a 2400s timeout.

| Version | With skill | Baseline (no skill) |
|---|---|---|
| **1.0.2** | **47 / 48** (7/8 cases all-pass, 0 timeouts) | 34 / 48 (2 timeouts) |
| 1.0.0 | 38 / 48 (2 timeouts) | 34 / 48 |

- **Ports finish:**
  - Python→Go: 6/6 in 797s. 1.0.0 timed out here.
  - Python→Rust: 7/7 in 1861s. 1.0.0 timed out at 5/7. The report is written as soon as the fixtures pass, and it says 4 inputs / 0 differences plus 400 generated / 0.
- **Java→Kotlin:** 1/6 → 6/6. The agent stays in the workspace and uses the existing toolchain.
- **Hard rules:** no installs, no cross-directory work, no "RESUME" hand-offs, and no files written for plan-only requests.
- **Triggering** (22 queries, 4 skills installed): 21/22. Refactor/port recall is 11/11 (1.0.0: 4/11). A database-migration request is no longer routed to this skill.
- **Caveats:**
  - Each case ran once.
  - The plan-only case still lacks an explicit out-of-scope list (4/5).
  - With the skill, runs are slower: 6 of 8 cases take over 680s.

被测模型 `glm-5.3-flash-external`（miniagent），2026-10-19，8 个用例，每例 1 次，超时 2400s。

- **得分：** 1.0.2 有技能 **47/48**，无技能基线 34/48，1.0.0 为 38/48。
- **完成情况：** 两个 Python 移植用例不再超时，Java→Kotlin 从 1/6 升到 6/6。
- **触发：** 召回 11/11（1.0.0 为 4/11）。
- **不足：** 每例只跑 1 次；仅出计划的用例仍缺范围外清单；有技能时耗时较长。

## Sources / 来源

The wording is original; ideas were synthesized from popular refactoring, migration and porting skills and literature. See [`references/sources.md`](references/sources.md) for the full list with links and licenses.

## License

MIT — see [LICENSE](LICENSE).
