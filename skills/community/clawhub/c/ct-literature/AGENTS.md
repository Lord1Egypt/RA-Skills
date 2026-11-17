# AGENTS.md · ct-literature

> A-tier public-intel skill of the `ct-` library (A 档 = non-confidential input). Systematic literature search (published-evidence base + CSM qualitative subset).
>
> **Tier (A/B two-tier):** this skill is **A 档 / A-tier** — its input is **non-confidential** (ordinary query terms only). Every data source is a public bibliographic API (OpenAlex / Europe PMC / preprint servers) and the skill processes **zero confidential input**. `network=public-retrieval` is an orthogonal sub-attribute of tier A (it answers "does the skill retrieve public sources?"), **not** a separate tier — ct- now classifies skills on the single axis of input sensitivity (A = non-confidential / B = confidential).

## Scope

- Retrieve published scholarly literature (OpenAlex primary; Europe PMC / Semantic Scholar optional) about a drug / disease / method.
- Normalize multi-source records into one de-duplicated evidence base; surface study-type distribution, yearly trend, and a safety/CSM subset.
- **Out of scope**: trial-registry metadata (→ `ct-registry`), FAERS disproportionality (→ `ct-safety`), full-text PDF download, paywalled content.

## Boundaries (do NOT blur)

- `ct-registry` answers *what trials exist*; `ct-literature` answers *what has been published*. Keep the object distinct — literature never fetches registry phase/status/enrollment; registry never fetches paper abstracts.
- `--safety` literature is qualitative; never feed it into FAERS PRR/ROR/IC. It only qualitatively corroborates `ct-safety`.

## Conventions

- Scripts: stdlib `urllib` for fetch (no hard `requests` dependency in fetch path); `normalize.py` / `report.py` are pure local.
- SAFE PREVIEW default: network runs only with `--run`.
- Zero confidential data or information input (A-tier).
- Common files (`scripts/i18n.py`, `references/language_policy.md`, `references/report_template.md`) are shared across the `ct-` library — do not fork them here; sync from the library instead. (`scripts/r_libs.py` was previously vendored but removed in v0.6.12 — this skill is pure Python and never calls R.)

## Self-improvement

- On repeated failure patterns, record to the workspace `.learnings/` per self-improving-agent rules.
- Source API changes (OpenAlex filter syntax, Europe PMC schema, S2 429 policy) → update `scripts/` + SKILL.md Data Sources, bump version in CHANGELOG.

## Standard inspection process (工作台自动化测试)

`workbench/` 工作台页面的标准检验流程已纳入 CT 家族统一框架 **`ctqa`**（位于 `ct-base/testing/ctqa/`，配置见本技能 `ctqa.config.json`）。原 `workbench/_tests/` 的静态套件以 **legacy 桥接**方式挂在 W0 层，现仅保留 `_support.py` + `test_static.py`（10 断言：语法 / i18n 覆盖 / DOM id 交叉引用 / 前后端事件协议四元核对）。**任何对 `workbench/` 或 CLI 事件协议的改动，发布前必须完整跑一遍**：

```bash
# 全量（推荐）
PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa run --skill ct-literature

# 只跑工作台相关层（快）
PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa run --skill ct-literature --layer W0 W1 W2B

# 先诊断可测性（层是否可用 / playwright / node 是否就绪）
PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa doctor --skill ct-literature
```

退出码 `0` = 绿灯（无阻断项）。报告落在 `tests/_ctqa_reports/`（html / json / junit / md）。

> ⚠️ **旧入口 `workbench/_tests/run_all.py` 已于 2026-10-29 删除**，不要再按旧文档执行；
> 文档里出现的 `run_all.py` 一律视为历史写法。实测 `ctqa --layer W0` 会同时跑
> W0 静态结构与契约（14 断言）与 legacy 桥接的 `test_static`（10 断言），合计 24 条。

### 390px 响应式与 §30.4 无障碍验收

ctqa 的 W2B 层固定 1280×900 视口，**不覆盖** ct-base `references/workbench_ui.md` §30.4
的移动端验收（390px `scrollWidth === clientWidth`、顶栏 ≤120px、三条 CSS 必备规则各 ≥1、
0 console errors、页脚在内容流）。该验收由本技能自有的
`workbench/_tests/test_responsive_390.py` 承担：自建 `server.py`（随机端口）、跑完即关，
已挂进 `ctqa.config.json` 的 skill_tests（W0 层，P1）。

```bash
# 单独跑（交付前 / 改工作台 CSS 后必跑）
C:/Tools/Anaconda3/python.exe workbench/_tests/test_responsive_390.py
```

退出码 `0` = 全部通过；截图落在 `workbench/_tests/responsive_390.png`。改 `workbench/app.css`
的顶栏 / 侧栏 / 断点后必须重跑——**注意 `@media (max-width:480px)` 与 768px 块在 390px 下
同时生效**，历史上曾因 480px 块把 `.wb-top-actions` padding 覆盖回 `8px 9px` 导致顶栏
高度超标（该块已于 2026-11-14 删除）。

核心防漂移：前后端两层事件协议四元核对；改任一侧事件协议必重跑 W0。详见 [references/workbench_testing.md](references/workbench_testing.md)。

## Standard inspection process (提示词使用方式测试)

提示词全链路（触发/规格构造/SAFE PREVIEW 闸门/跨轮连贯/批量规格/Coze 信封/E2E dry-run）同样纳入 `ctqa`。原 `tests/prompt_usage/` 的七层套件以 **legacy 桥接**挂在 P5/C0 层，现仅保留 `_support.py` + `test_l6_coze.py`（Coze 信封 11-key 硬白名单脱敏 + 真实白名单发送 e2e）。**任何对规格构造、预览闸门、merge_spec、batch parser、Coze 信封（`adapters/bug_report.py`）的改动，发布前必须完整跑一遍**：

```bash
# 提示词与 Coze 契约相关层
PYTHONPATH=../ct-base/testing C:/Tools/Anaconda3/python.exe -m ctqa run --skill ct-literature --layer P3 C0
```

核心防漂移：SAFE PREVIEW 闸门（monkeypatch 证明无 `--run` 时 `run()` 0 次调用）、Coze 11-key 硬白名单（`sanitize_report` 剔除越权键）、merge_spec 唯一权威副本在 `ct-base/scripts/`。真实 Coze e2e 由 `CT_COZE_E2E=1` 开启（白名单已授权）。测试子进程一律英文主题。详见 [references/prompt_usage_testing.md](references/prompt_usage_testing.md)。

## Version

Current: v1.0.0 (A-tier public-intel literature search skill; aligned with SKILL.md). See SKILL.md `version:` for the authoritative number.
