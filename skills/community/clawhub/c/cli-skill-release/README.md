# cli-skill-release · 零依赖 Python CLI 技能发布工程

> **English TL;DR** — `cli-skill-release` is a **release-engineering toolkit for zero-dependency Python CLI agent skills**. Its core is a real, runnable tool `releaser.py` (17 subcommands) that doesn't just *describe* how to publish — it *does* the work: scans publish traps, scores readiness 0–100 with **functional verification that actually boots your CLI**, gives a CI quality gate, scaffolds a project, and builds marketplace publish intel. Where competitors (skill-lint, jeremyknows/publish-skills, skill-creator) only hand you a document to follow, we **execute the engine**. MIT-0, zero dependencies (stdlib only), 78 passing tests.

> **一句话（中文）**：把"以 Python CLI 形式交付的 WorkBuddy / ClawHub 技能做成可发布项目并上架"的全流程固化。核心是零依赖 `releaser.py`（17 个子命令）：主动扫描发布陷阱、给 0–100 就绪分（含★功能级验证真跑 CLI）、CI 质量门禁、脚手架、推送上架、链回徽章。竞品（skill-lint / jeremyknows / skill-creator）只给文档让你照着做，我们**替你把引擎跑起来**。MIT-0，零依赖，78 测试全绿。

[![releaser readiness](https://raw.githubusercontent.com/cdhewei/cli-skill-release/main/readiness-badge.svg)](https://clawhub.ai/cdhewei/cli-skill-release)
[![License: MIT-0](https://img.shields.io/badge/license-MIT--0-blue.svg)](#license)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB.svg)](#)
[![Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)](#)
[![Tests](https://img.shields.io/badge/tests-77%20passing-brightgreen.svg)](#tests)
[![Updated](https://img.shields.io/badge/last%20updated-2026--09--24-brightgreen.svg)](#)

---

## Why not just lint? / 为什么不是又一个 lint 工具

Skill-lint / agent-skill-linter / @effectorhq/skill-lint / jeremyknows/publish-skills only check **paperwork** (frontmatter, license field, file structure). `releaser.py` is the **only** tool that **actually runs your CLI** — compile + import + `--help` smoke test — to prove it boots. It catches "looks perfect, crashes on run" skills that every other linter misses. That functional verification is our differentiator.

竞品（含 skill-creator）只查"纸面合规"：frontmatter、license 字段、文件结构。`releaser.py` 是**唯一**把你的 CLI **真正执行起来**（compile + import + `--help` 烟测）证明它能启动的工具——专门兜住"格式完美、一跑就崩"的技能。★功能级验证就是我们的差异化价值。

### Competitor comparison / 竞品对比

| Capability / 能力 | skill-lint 类 | jeremyknows/publish-skills | skill-creator（写） | **cli-skill-release（发+情报）** |
|---|---|---|---|---|
| 校验发布陷阱 | 纸面 | 静态清单 | — | ✅ **主动扫描 + 0-100 就绪分** |
| ★功能级验证（真跑 CLI） | ❌ | ❌ | ❌ | ✅ **compile+import+--help 真 boot** |
| CI 质量门禁（gate） | ❌ | ❌ | ❌ | ✅ **readiness-as-a-service** |
| 市场缺口情报（gap/curate） | ❌ | ❌ | ❌ | ✅ **该造什么主动告诉你** |
| 长尾诊断（diagnose） | ❌ | 静态 | ❌ | ✅ **症状→根因→修复** |
| 上架前清单（preflight） | ❌ | 部分 | ❌ | ✅ **市场定制清单** |
| 链回徽章（badge） | ❌ | ❌ | ❌ | ✅ **便于引用与致谢** |
| 可执行工具 + 测试 | ❌ | ❌ | ❌ | ✅ **CLI + pytest（78 全绿）** |
| 发布侧治理（registry/recheck） | ❌ | ❌ | ❌ | ✅ **状态层 + 生命周期** |

---

## 30-second intro / 30 秒了解它

发 AI 技能 = 把你的代码交给别人跑。但生态里**没人真正帮你确认过它能跑、合规、会被找到**。

`cli-skill-release` 补上这一环：

| 别人帮你「写文档」 | 它帮你「发出去 + 被找到 + 链回致谢」 |
|---|---|
| 给你清单，你自己照着点 | **主动扫描陷阱 + 0-100 就绪分** |
| 格式过了，一跑就崩 | **★功能级验证真跑 CLI，崩不了** |
| 不知道市场缺什么 | **gap / curate 告诉你该造什么** |
| 发完即终 | **registry / recheck 持续治理** |
| 没人帮你传 | **badge 链回，便于引用致谢** |

一句话：**如果你只想照文档发技能，竞品够用；如果你要在乎发得稳、被找到、能引用致谢，用 cli-skill-release。**

```bash
python releaser.py promote --path .   # 一键生成推广素材（含 30 秒电梯演讲 EN+中文）
```

---

## Install / 安装

```bash
git clone https://github.com/cdhewei/cli-skill-release.git
cd cli-skill-release
# 零依赖，仅标准库，无需 pip install
python releaser.py doctor --path .
```

## Quick start / 快速开始

```bash
python releaser.py validate --path ./my-skill          # 0-100 就绪分 + 功能验证
python releaser.py diagnose --symptom "LICENSE 显示 Other"   # 长尾诊断
python releaser.py preflight --market clawhub          # 上架前检查清单
python releaser.py badge --path . --output readiness-badge.svg   # 链回徽章
python releaser.py promote --path .                    # 发布说明工具箱
python releaser.py release --path . --dry-run          # 人工导入情报
```

---

## 17 subcommands / 17 个子命令

| Subcommand | 作用 / What it does |
|---|---|
| `scaffold <name>` | 一键生成带 CI 的完整可发布骨架 / scaffold a CI-ready skeleton |
| `validate --path <dir>` | **★杀手锏**：主动扫描 + 0-100 就绪分 + ★功能验证 + ★安全红线凭据扫描 / active scan + score + functional + secret verify |
| `secretscan --path <dir>` | **★安全红线**：专项扫描硬编码密码/授权码/API Token（独立于就绪分）/ dedicated credential-leak scan |
| `gate --path <dir> --min 90` | **CI 门禁**：就绪分低于阈值即非零退出 / quality gate for pipelines |
| `inventory [--roots ...]` | 治理：本机技能哪些能发 / which installed skills can ship |
| `gap [--roots ...]` | **市场情报**：本机覆盖 + 组合缺口 / market gap intelligence |
| `selfcheck [--path .]` | 零依赖校验：扫 import / zero-dep check |
| `bump [--type patch]` | 升版本号 + 补 CHANGELOG / bump version |
| `release --path .` | git 推送(需 `--push`) + clawhub 发布(需 `--publish`) / push + publish intel |
| `publish --github --clawhub` | **★多站上架编排**：显式逐站授权上传 GitHub/ClawHub（安全闸门前置）/ multi-registry orchestrator |
| `badge --path <dir>` | **★链回徽章**：就绪分徽章 SVG + 链回片段 / readiness badge |
| `promote [--path <dir>]` | **★发布说明工具箱**：徽章+要点说明+社媒文案 / promo toolkit |
| `diagnose --symptom "..."` | **★长尾诊断**：症状→根因→修复 / symptom→root-cause→fix |
| `preflight [--market clawhub]` | **★上架前清单**：市场定制 / market-specific checklist |
| `registry [list\|show\|add]` | **★状态层**：已发布技能账本 / published-skill ledger |
| `recheck [<slug>]` | **★生命周期**：再校验漂移/弃用 / drift re-check |
| `selfdemo` | **★自证底座**：全量自证（主张即演示）/ prove-by-running |
| `curate [--roots ...]` | **★供给侧策展**：主动告诉生态该造什么 / what to build next |
| `doctor [--path <dir>]` | 自检本工具 / self-check |

---

## Long-tail FAQ（长尾问题，直接回答你搜到的）

### skill publish checklist / 技能发布前检查清单
Run `python releaser.py preflight --market <clawhub|skillhub|agentskills|generic>` for a market-specific checklist (MIT-0, skill-card.md rename, Topics ≤48, 3 categories, text-only files, GitHub topics). 中文见 `preflight --market clawhub`。

### Is my skill ready to publish? / 我的技能能不能发
`python releaser.py validate --path .` 给 0–100 发布就绪分（含 ★功能验证真跑 CLI）。分数 ≥90 再发 / score ≥90 before you publish.

### What am I missing before I push this skill to GitHub? / 还差什么
Run `validate` + `preflight`. Common misses: missing LICENSE (MIT-0), non-ASCII copyright holder (shows Other), `skill-card.md` reserved-name conflict, Topics >48 chars, doctor subcommand missing `--path` (CI reds).

### Audit this skill against the Agent Skills spec
`gh skill publish --dry-run` (agentskills.io) + `releaser.py validate`. We cover spec compliance **and** functional boot — most checklists (e.g. jeremyknows/publish-skills) stop at paperwork.

### skill LICENSE 显示 Other / LICENSE shows Other
Cause: LICENSE lacks a recognizable SPDX id, or the copyright holder name is non-ASCII (e.g. Chinese "何巍"). Fix: write MIT-0 verbatim with an ASCII holder name ("He Wei"); verify via `api.github.com/repos/{owner}/{repo}/license`. See `diagnose --symptom "LICENSE 显示 Other"`.

### pytest exit code 2 / CI 一直红
Cause: `tests/` imports need `conftest.py` sys.path injection (CLI injects at module level, CI doesn't). Exit codes: 2=collection error, 1=test fail, 0=pass. Fix: add `tests/conftest.py`; `releaser.py gate` blocks the same trap. See `diagnose --symptom "pytest exit code 2"`.

### ClawHub publish guide / ClawHub 上架教程
MIT-0 forced, `skill-card.md` is reserved (rename it), Topics whole-string ≤48 chars, account age ≥1 week, pick 3 categories, README required, text-only files. `releaser.py release` builds the import intel; if `clawhub` CLI is installed + logged in, it publishes for real.

### 凭据/密码/授权码会不会被发到 GitHub？ / Will my credentials leak to GitHub?
No. `releaser.py secretscan` (and the `validate`/`release` security-redline gate, weight 12) **mandatorily scans the whole skill for hardcoded passwords / auth-codes / API tokens before publish**; on a hit it FAILs and `release`/`publish` hard-block commit/push/publish. Environment-variable references (`os.environ.get(...)` / `${...}`) are treated as safe. Reports are **redacted** — plaintext is never echoed. If a real secret was already committed, rotate it immediately, then `git filter-repo --path <file> --invert-paths` to scrub history.

### 如何一次上传到多站（GitHub / ClawHub / 虾评 / WorkBuddy）？ / How do I upload to multiple registries at once?
Use `publish` — the explicit per-site orchestrator. `releaser.py publish --path .` only proofreads + previews (touches nothing remote); add `--github` and/or `--clawhub` to explicitly authorize each site (`publish --github --clawhub`). **No flag = no remote write**, and the security red-line gate always runs first, so a corrected/new skill can be dispatched safely without silent egress. 虾评(xiaping.coze.site) and WorkBuddy SkillHub(open.workbuddy.cn) are reserved this round (no public API); their flags print manual-upload links and will become truly automatic once their endpoints/bots are wired in.

### 技能搜不到 / make my skill discoverable
The SKILL.md `description` is the vector-search match surface; `tags` decide adjacency; GitHub topics feed external indexers (SkillsMP / skillsdirectory). Write bilingual trigger phrases into `description`, add `tags`, and set repo topics: `agent-skills claude-skills codex-skills skill-md ai-agents`.

---

## Back-link badge / 链回徽章（便于引用与致谢）

Every user runs `badge` and pastes the readiness badge into their skill's README. The badge links back to this page. A visitor clicks → uses the tool → if they publish their own skill, they may paste the badge too — natural referencing and attribution. One download, organic referencing.

每个使用者跑一次 `badge`，把 readiness 徽章贴进自己技能的 README，徽章链回本页。访客点入 → 用工具 → 若发布自己的技能，也可贴同一徽章——形成自然的引用与致谢。一次下载，自发式引用。

## License / 许可证
MIT-0. Zero dependency (standard library only). 完整中文手册见 [`SKILL.md`](SKILL.md)，英文手册见 [`SKILL.en.md`](SKILL.en.md)。
