<div align="center">

# Council Pilot

**Give Claude Code a one-liner. Get a production-quality project.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://docs.anthropic.com/en/docs/claude-code)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Council Pilot is a Claude Code skill that builds an expert council from public sources, then autonomously drives your project through build-score-debug loops until it reaches **100/100 maturity**.

No micromanagement. No prompt-chaining. One sentence, hours of focused work.

</div>

---

```
/council-pilot "Build a real-time collaborative whiteboard with WebSocket sync"
```

That's it. Council Pilot takes over: discovers domain experts, distills their reasoning into advisory lenses, forms a council, then loops build → score → debug → rescore until the council agrees the project is production-ready. Then it submits a PR.

## Why This Is Different

Most AI coding tools give you one-shot answers. You prompt, you get code, you prompt again. Council Pilot is fundamentally different:

**1. It works autonomously for hours.** Give it a repo and a one-liner. It plans, builds, tests, critiques its own work, and iterates. A typical run takes 2-3 hours and produces a complete version iteration — not a snippet, not a suggestion, a finished project.

**2. It self-critiques like a senior engineer.** The expert council isn't decorative. Each lens is distilled from real public sources — reasoning patterns, evidence preferences, critique habits, known blind spots. The council debates every scoring decision. The skeptic challenges high scores. The advocate defends low ones. Points are earned, not given.

**3. It's infinitely adaptable.** The expert library is built from scratch for each domain. AI reliability? Finance risk? Game engine design? Council Pilot discovers the right experts, distills their public knowledge, and builds a project guided by their actual reasoning patterns. Swap domains, get a completely different council.

## How It Works

```
YOUR IDEA
    │
    ▼
 INIT ──► DISCOVER ──► DISTILL ──► COUNCIL
                                        │
                              First score = 0/100
                                        │
                    ┌───────────────────┘
                    ▼
               BUILD ──► DEBUG ──► RESCORE
                    ▲                    │
                    │          score < 100│
                    │                    ▼
                    ┗━━━━ GAP_FILL ━━━━━┛
                                         │
                               score = 100 + all PASS
                                         │
                                         ▼
                                      SUBMIT (PR)
```

**Phases 1-4** (setup): Parse your idea into a domain spec. Web-search for real domain experts. Distill their public work into reasoning lenses. Form an expert council with chair/reviewer/advocate/skeptic roles.

**Phases 5-9** (loop): Build project code guided by expert lenses. Run 6-stage verification (build, types, lint, tests, security, diff). Rescore through adversarial council debate. Fill gaps by adding new experts or targeting weak axes. Repeat.

**Phase 10** (submit): Push branch, create PR with full maturity report.

## The Scoring Rubric

Each axis is scored 0-25 by the expert council. Convergence requires **100/100**:

| Axis | What It Measures | How You Earn Points |
|------|-----------------|---------------------|
| **Breadth** | Domain coverage | Every sub-domain addressed, no gaps |
| **Depth** | Expert profile richness | Source-backed reasoning, not surface-level |
| **Thickness** | Practical implementability | Code compiles, tests pass, edge cases handled |
| **Effectiveness** | Problem-solution fit | Actually solves the stated problem, not just looks correct |

100/100 is intentionally hard. The council won't award it until they can't find meaningful improvements.

## Source Gates

Expert quality is gate-kept, not assumed:

- **Tier A**: Official pages, papers, books, formal lectures — defines core beliefs
- **Tier B**: Interviews, essays, course notes — shapes reasoning patterns
- **Tier C**: Social posts, forums, summaries — context only, cannot define core claims

A candidate needs at least 1 Tier A + 1 Tier B source. No exceptions.

## Quick Start

```bash
# Install
git clone https://github.com/wd041216-bit/council-pilot.git ~/.claude/skills/council-pilot
```

Restart Claude Code, then:

```
/council-pilot "Build a LLM hallucination detection library with benchmarking"
```

Or use the CLI standalone:

```bash
# Initialize forum
python3 scripts/expert_distiller.py init \
  --root ./forum --domain "AI Reliability" --topic "LLM hallucination detection"

# Add expert candidates and sources
python3 scripts/expert_distiller.py candidate \
  --root ./forum --domain "AI Reliability" \
  --name "Samuel Bowman" --reason "Leading researcher in LLM evaluation"

python3 scripts/expert_distiller.py source \
  --root ./forum --expert-id samuel-bowman \
  --tier A --title "Official profile" \
  --url "https://www.cs.ubc.ca/~bowman/" --note "Research group homepage"

python3 scripts/expert_distiller.py source \
  --root ./forum --expert-id samuel-bowman \
  --tier B --title "Public lecture or interview" \
  --url "https://example.com/samuel-bowman-interview" --note "Reasoning and evaluation context"

python3 scripts/expert_distiller.py candidate \
  --root ./forum --domain "AI Reliability" \
  --name "Margaret Mitchell" --reason "Responsible AI and model evaluation perspective"

python3 scripts/expert_distiller.py source \
  --root ./forum --expert-id margaret-mitchell \
  --tier A --title "Official profile" \
  --url "https://m-mitchell.com/" --note "Research homepage"

python3 scripts/expert_distiller.py source \
  --root ./forum --expert-id margaret-mitchell \
  --tier B --title "Public talk or interview" \
  --url "https://example.com/margaret-mitchell-interview" --note "Responsible AI context"

# Audit, profile, form council, score
python3 scripts/expert_distiller.py audit --root ./forum --expert-id samuel-bowman
python3 scripts/expert_distiller.py audit --root ./forum --expert-id margaret-mitchell
python3 scripts/expert_distiller.py profile --root ./forum --domain "AI Reliability" \
  --expert-id samuel-bowman --name "Samuel Bowman"
python3 scripts/expert_distiller.py profile --root ./forum --domain "AI Reliability" \
  --expert-id margaret-mitchell --name "Margaret Mitchell"
python3 scripts/expert_distiller.py council create --root ./forum --domain "AI Reliability"
python3 scripts/expert_distiller.py score --root ./forum --domain "AI Reliability"
python3 scripts/expert_distiller.py report --root ./forum --domain "AI Reliability" --format markdown
```

The standalone example demonstrates command wiring. For a real council, replace
the `example.com` Tier B placeholders with actual public interviews, talks,
essays, or course notes before treating the sources as evidence.

## CLI Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize forum root and domain |
| `candidate` | Queue an expert candidate |
| `source` | Add a tiered source to a dossier |
| `audit` | Audit candidate for promotion readiness |
| `profile` | Create expert profile skeleton |
| `index` | Rebuild forum index |
| `validate` | Validate profile completeness |
| `discover` | Discover candidates from file or SKILL mode |
| `fill` | Output fill prompt for profile distillation |
| `council` | Manage councils (create/add-member/list/show) |
| `score` | Score artifact against expert council |
| `coverage` | Analyze expert coverage gaps |
| `refresh` | Check source freshness |
| `build` | Record build context |
| `report` | Generate maturity report (JSON or Markdown) |

## Agents

| Agent | Role |
|-------|------|
| `expert-researcher` | Discovers candidates via web search, collects sources |
| `profile-distiller` | Fills expert profiles from source content |
| `forum-moderator` | Orchestrates council debate and scoring |
| `project-builder` | Generates code guided by expert lenses |
| `maturity-scorer` | Adversarial 4-axis scoring |
| `gap-analyst` | Identifies coverage gaps and recommends next steps |

## Dynamic Expert Addition

The pipeline adds new experts mid-loop when the gap analyst identifies uncovered sub-domains:

1. Gap analyst flags missing expertise
2. Expert researcher discovers 1-2 targeted candidates (fast-track)
3. Minimum sources collected, abbreviated audit, added to council
4. Fast-tracked experts start with capped weight (0.2 vs 0.3)
5. After 2 scoring cycles, fast-track flag is removed

Max 2 new experts per iteration. Council size capped at 10.

## Failure Recovery

| Failure | What Happens |
|---------|-------------|
| Max iterations (default: 10) | Pause, generate report, print state |
| Build failure (3 retries) | Log failure, feed to gap analyst |
| Score regression (>10 points) | Pause, revert to previous artifact |
| Context window pressure | Write state to disk, compact, resume |

## Trust Model

Expert profiles are **analysis lenses**, not primary evidence. Council Pilot:

- Requires Tier A + Tier B sources before promotion
- Never uses Tier C to define core beliefs, reasoning, or quotes
- Preserves source disagreements instead of smoothing them away
- Never fabricates quotes or invents private beliefs
- Current data and user constraints always outrank expert memory

## Output Layout

```
forum/
├── forum_index.json              # Forum overview
├── pipeline_state.json           # Current phase, scores, history
├── domains/<domain_id>.json      # Domain definition
├── candidates/<expert_id>.json   # Expert candidates
├── source_dossiers/<id>.json     # Collected sources per expert
├── promotion_audits/<id>.json   # Promotion gate results
├── experts/<id>/profile.json     # Filled expert profiles
├── experts/<id>/distillate.md    # Distilled reasoning markdown
├── councils/<council_id>.json    # Council definitions with roles
├── scoring_reports/<id>.json    # Per-iteration scoring reports
├── gap_analyses/<id>.json       # Gap analysis with recommendations
└── build_logs/<id>.json         # Build context per iteration
```

## References

- [`references/profile-contract.md`](references/profile-contract.md) — Expert profile JSON contract
- [`references/source-gates.md`](references/source-gates.md) — Source tier rules
- [`references/scoring-rubric.md`](references/scoring-rubric.md) — 4-axis maturity rubric
- [`references/council-protocol.md`](references/council-protocol.md) — Council debate rules
- [`references/loop-state-machine.md`](references/loop-state-machine.md) — Pipeline state machine
- [`references/build-integration.md`](references/build-integration.md) — Build/debug cycle spec
- [`references/github-submission.md`](references/github-submission.md) — Submission protocol

---

<div align="center">

**[English](#why-this-is-different) | [中文](#中文说明)**

</div>

---

## 中文说明

**给 Claude Code 一句话，它还你一个生产级项目。**

Council Pilot 是一个 Claude Code 技能，从公开来源构建专家委员会，然后自主驱动项目通过构建-评分-调试循环，直到达到 **100/100 成熟度**。

### 三个核心差异

**1. 自主工作数小时。** 给它一个仓库和一句话，它自主规划、构建、测试、自我批评、迭代。一次典型运行耗时 2-3 小时，产出一个完整的项目版本——不是代码片段，不是建议，是一个可交付的项目。

**2. 像资深工程师一样自我批评。** 专家委员会不是摆设。每个专家视角都从真实公开来源提炼——推理模式、证据偏好、批评习惯、已知盲区。委员会对每个评分决策进行辩论。质疑者挑战高分，辩护者维护低分。分数是挣来的，不是给的。

**3. 无限适配。** 专家库为每个领域从零构建。AI 可靠性？金融风控？游戏引擎设计？Council Pilot 发现合适的专家，提炼他们的公开知识，按照他们的实际推理模式构建项目。换一个领域，得到一个完全不同的委员会。

### 快速开始

```bash
# 安装
git clone https://github.com/wd041216-bit/council-pilot.git ~/.claude/skills/council-pilot
```

重启 Claude Code，然后：

```
/council-pilot "构建一个带 WebSocket 同步的实时协作白板"
```

### 评分体系

每轴 0-25 分，收敛需要 **100/100**：

| 轴 | 衡量什么 | 如何获得分数 |
|-----|---------|------------|
| **广度** | 领域覆盖 | 每个子领域都被覆盖，没有盲区 |
| **深度** | 专家丰富度 | 有来源支撑的推理，不是表面文章 |
| **厚度** | 实际可执行性 | 代码编译通过、测试通过、边界情况处理 |
| **有效性** | 问题-方案匹配 | 真正解决了问题，而不是看起来正确 |

### 信任模型

专家档案是**分析视角**，不是主要证据。Council Pilot：

- 必须有 A 层 + B 层来源才能晋升
- 永远不用 C 层来源定义核心信念
- 保留来源间的分歧，而不是抹平它们
- 永远不编造引用或捏造私人观点
- 当前数据和用户约束始终优先于专家记忆

---

<div align="center">

**License: MIT** · **Issues & PRs welcome** · **Star if you find it useful**

</div>
