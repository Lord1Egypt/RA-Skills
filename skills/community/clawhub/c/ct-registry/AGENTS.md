# AGENTS.md — ct-registry v1.0.1

## Overview

`ct-registry`: Cross-source search of global clinical-trial registries (ClinicalTrials.gov /
China CDE / China ChiCTR / EU CTR / ISRCTN / DRKS / WHO ICTRP) and normalized aggregation,
for trial planning, de-duplication, control-design benchmarking and competitive intelligence.
PubChem provides drug→target mapping. **WHO ICTRP is a Tier-2 external service (re-added
2026-07-27)** via `search_ictrp.py` (`source="who"`); one call mirrors 14+ registries
(jRCT / DRKS / ANZCTR / ISRCTN / CTRI / …), expanding coverage — its bridge/de-dup value is
reinforced (not merely replaced) by `aggregate.py`. **The SAME unified endpoint also serves China
CDE** via `source="chinadrugtrials"` (`search_ictrp.py --source chinadrugtrials`; `ct_registry.py --with-cde` defaults there). The standalone `ct-searchcde.coze.site/run` endpoint is **RETIRED 2026-08-12** — `--cde-legacy` is now a no-op warning that auto-routes to the unified endpoint. **one token (`config/ictrp.dat`) covers both WHO and CDE**.
**WHO-coverage fallback policy (2026-07-28, revised 2026-07-28):** when `ct_registry.py --with-ictrp` is set, WHO ICTRP is the PRIMARY aggregator and the national registries it covers (CT.gov, EU-CTR, ISRCTN, DRKS, ChiCTR) become FALLBACK-ONLY — skipped on WHO success, retrieved independently + aggregated ONLY if WHO cannot retrieve (prompt via `[ct_registry][FALLBACK-PROMPT]`, then re-run with `--fallback-covered`). **EXCEPTION — CDE is always independent:** China CDE (`--with-cde`) is never skipped on WHO success and never a fallback, because WHO's English-title matching misses Chinese-registered trials; CDE is searched on its own whenever `--with-cde` is set. PubChem enrichment is unaffected. Without `--with-ictrp`, legacy behavior is preserved. Sources split into Tier 1 (direct, pure
HTTP: CT.gov + EU CTR + PubChem) and Tier 2 (external workflow, Bearer token, no browser:
CDE / ChiCTR / ISRCTN / DRKS / WHO ICTRP). Reads public registry data via public retrieval;
ordinary input + public retrieval; B-tier quickly-adoptable. Natural-language parameter
confirmation follows `references/search_menu.md` (ct-base §6.1).

### Search procedure (mandatory order, v0.3.2)
1. **Scope first** — decide which registries to cover. If scope = {WHO ICTRP, CDE}, those TWO
   endpoints already cover CT.gov / EU-CTR / ChiCTR / ISRCTN / DRKS (WHO mirrors them) + China CDE
   (independent), so do NOT separately hit CT.gov/EU-CTR/ChiCTR/ISRCTN/DRKS. Only fall back to
   direct Tier-1 sources if WHO is unreachable (no token / 403) — via FALLBACK-PROMPT, no auto fan-out.
2. **Keywords + translation** — derive per-source terms and translate: EN for CT.gov/WHO/PubChem
   (`Type 2 Diabetes` + `DPP-4 inhibitor`); ZH for CDE (`II型糖尿病`/`2型糖尿病` + `DPP-4抑制剂`,
   strip the `类` suffix; never `DPP-4抑制剂类`). Category terms → use acronym/full-name or enumerate
   members, not a bare class suffix.
2b. **Prefer advanced search when the prompt has a parameter combo (v0.3.14)** — WHO AdvSearch
   exposes **Phases** + condition/intervention/sponsor/country/date fields; CDE AdvSearch exposes
   登记号/适应症/药物名称/药物类型/申请人/试验状态 (NO phase filter). When the user's prompt
   contains a combination (drug + phase, disease + sponsor + country + year, …), build a **structured
   payload** instead of bare keyword: WHO → `--who-condition/--who-intervention/--who-sponsor/
   --who-country/--who-phase` (auto `mode=combined`); CDE → `--reg-no/--indication/--drugs-name/
   --drugs-type/--appliers/--trial-status` (auto `is_advanced_search`). ⚠️ `--who-phase` server-side
   filtering **under-captures combined/numeric phases** (verified: Olverembatinib +I/II → 2 of ~19
   true I/II); use it only as a coarse narrowing, and always re-validate phase on detail-normalized
   `phase` (authoritative). Full field→CLI map in SKILL.md "Advanced search (高级检索)".
3. **Execute + return** — direct sources run free (`--run`, no quota); external-workflow sources
   ride the shared endpoint (**1 count PER DEMAND** via `usage_guard`: WHO+CDE / keyword tweaks /
  repeats sharing one `demand_id` collapse to a single count; daily cap = 1000 demands; **local long-lived token, no refresh needed**).
   Then `normalize → aggregate → report`; PDFs never auto-download (only `--download-docs` on
   explicit user request). Full text in SKILL.md "Search procedure" section.

### Resource-usage policy (v0.3.1, enforced in code)
- WHO / CDE retrieval is **free** but rides a **shared** third-party endpoint (Coze /run); follow
  **minimal shared-resource occupation**. Bulk retrieval needs → direct the user to **contact the
  author (Wintone) for coordination**.
- **Hard daily cap = 1000 demands** (a demand = one `ct_registry.py --run`, or one agent task of
  step-by-step retrievals sharing a `demand_id`). WHO+CDE / keyword tweaks / repeats inside the SAME
  demand all collapse to **1 count** — charged per `demand_id`, not per raw HTTP call. Counts only
  real `--run` network calls (WHO/CDE/ChiCTR/ISRCTN/DRKS); preview / `--store-token` / direct sources
  CT.gov/EU-CTR/PubChem are NOT counted. Rolls over at local midnight. **Each call prints the
  remaining quota** (a repeat of an already-counted demand prints "already counted, not re-charged");
  at 1000 demands the call is BLOCKED with "come back tomorrow". Counter: `config/usage.json` (fail-open on IO error).
- **PDFs are NEVER auto-downloaded**: `download_docs.py` lists links by default and downloads only
  with `--yes`; the orchestrator downloads only when `--download-docs` (explicit user request) is set.
- Enforcement: `scripts/usage_guard.py` (`check()`), called from `search_ictrp.py`,
  `CDE/search_cde_workflow.py` (archived standalone), and `extsvc_client.dispatch()`; `ct_registry.py` also prints the policy
  in preview mode.

---

## Core Rules (inherited from ct-base, applies library-wide)

### 1. R / Python Environment Detection
- Python via Anaconda (`C:\Tools\anaconda3\python.exe`); do not hardcode paths.

### 2. Code Execution
- **Default: SAFE PREVIEW (dry-run).** Scripts show the planned call; execute only with `--run`.
- Temp files written to system temp, auto-cleaned.

### 3. Language Detection (see references/language_policy.md)
- Default English; auto-switch to Chinese on Chinese-OS.
- Common modules prepare EN+ZH; code output always English.

### 4. Security Red Line (inherited from ct-base, highest priority)
- **Read public registry data via public retrieval; zero confidential data or information input.** This skill is B-tier quickly-adoptable.
- CDE primary automatable path is the **unified endpoint** (`search_ictrp.py --source chinadrugtrials` → third-party endpoint `ct-search.coze.site/run`), shared with WHO ICTRP. It sends public query terms plus non-content request metadata (`query_origin` machine-hash for abuse-limiting/attribution, `skill_version`, `entry_point`, `user_language`, `demand_id` — disclosed in README egress section) and REQUIRES a Bearer token. The optional `--cde-api-key` fast path goes to the DXY commercial CDE-mirror API (`api.dxy.cn`), opt-in, never to the unified endpoint. The legacy **standalone** CDE workflow (`CDE/search_cde_workflow.py` → `ct-searchcde.coze.site/run`, archived under `CDE/`, NOT shipped) is **RETIRED 2026-08-12**; the `--cde-legacy` switch is now a no-op warning that auto-routes to the unified endpoint. Paste-mode Playwright / `parse_cde.py` local parse stays a no-egress fallback. Always disclose "data passes through a third party" for any workflow path.
- All user strings whitelist-validated to prevent injection / RCE.
- `permissions` block explicitly declared at top level of SKILL.md.
- **Tokens (`config/*.dat`) are obfuscated PUBLIC shared Coze/ICTRP credentials** (not personal). Classified as public per ct-base §5; excluded from the published package by design (installers supply their own via `--store-token` / env, or a deploy populates the blob). Never paste tokens in chat.

### 5. Reuse from base
- Copied from `ct-base`: `i18n.py`, `r_libs.py`, `language_policy.md`, `icon.svg`. Business scripts live in `scripts/`.（注：`report_template.md` 原为 ct-base 拷贝的样本量/效能模板，与注册检索无关，已于 v0.3.82 移出至 `_archived_orphans/`，不随技能发布。）

---

### 6. Coze 出站调用规范 (ct-base §5)
- 本技能经 Coze 统一端点 (`ct-search.coze.site/run`) 检索 CDE / WHO ICTRP / ChiCTR / ISRCTN / DRKS，属**出站调用**。代理（agent）在发起任何出站前，须严格遵循以下链路（全库统一，对齐 ct-advisor 实测实现）：
  - **① 首次出站确认门 + 白名单持久化（§5.25-43）**：调用方脚本内置 `[AUTH-BLOCK]` 授权门控——未授权端点会向 stderr 输出 `[AUTH-BLOCK] outbound to <endpoint> requires user confirmation.` 并返回空集（不阻断本地逻辑）。代理捕获该信号后，向用户展示**统一确认文案**（按会话语言选中文/英文，禁止出现 step/流程/内部术语）：
    - 中文：`⚠️ [ct-registry] 需要把您发送的检索词送到外部服务器进行智能分析：目标服务器：<endpoint> / 发送内容：您的公开检索词（不含任何个人身份信息）/ ⚠️ 重要提示：本技能的本地参考资料库有限，大部分检索依赖云端服务器。如不同意发送，将无法使用云端数据库。是否允许本次发送？确认后本会话内不再重复询问。`
    - English: `⚠️ [ct-registry] needs to send your query to an external server for intelligent analysis. Target server: <endpoint>. Content sent: your public search terms (no personal identifying information). Note: this skill's local reference library is limited; most retrieval relies on the cloud server. If you decline, the cloud database will be unavailable. Allow this send? You will not be asked again this session.`
    - 用户确认后，将端点加入 `config/config.json` 的 `auto_approve_endpoints` 数组（**代理绝不自行改写 `config.json`**，须由用户确认触发并告知用户）。已预置端点（unified endpoint）实际永不弹确认。
  - **② forward 前唯一流程通知（§5.46）**：在真正发起 Coze 调用前，向用户发**恰好一条**简短通知（`正在调用云端分析引擎，请稍候…` / `Please wait while the cloud analysis runs…`），且仅此一条——不得重复、不得追加任何 step / 流程类播报。其余内部状态（HARD GATE、难度标签、fallback 机制）**绝不**出现在用户可见文本。
  - **③ Coze 失败诊断须先确认（§5.47）**：stderr 出现 `FALLBACK` / `ProxyError` / `Timeout`，或 stdout 提示诊断时，**先问用户**"Coze 云端服务暂时不可用，是否允许我自动诊断排查？"；允许 → 运行一次 `check_coze.py` 定位根因（死代理残留 / 断网 / token 缺失 / 端点不可达）并修复重试；拒绝 → 交付本地答案并附显著警告"无法连接 Coze 服务，答案未经过精校，请谨慎使用"。
  - **④ need_params 缺失须向用户确认（§5.48）**：Coze 返回 `need_params`（定界包裹内 `<<<CT_NEED_PARAMS>>>` 块）→ 向用户逐项询问缺失参数（**绝不**编造），重建卡片 JSON（保留 `draft_answer` / `need_tool`、填 `params`、保留 `original_question`）后重跑。
  - **⑤ 代理残留自动重试（§5.49）**：`requests` 抛 `ProxyError` / `ConnectionError`（Windows 系统代理残留 → WinError 10061）时，调用方已内置自动绕过系统代理（`proxies={"http":None,"https":None}`）直连重试一次；直连仍不可达则照常向上抛 fallback。代理无需手动干预。
  - **⑥ 出站 payload 发送前脱敏（§5.50）**：调用方已对发往 Coze 的 payload 经 `_sanitize_payload()` 剥离 PII（身份证 / 手机号 / 邮箱）后再发送；脚本绝不回显 token / payload / draft 明文（预览模式仅打印结构化请求，不含凭据）。
  - 完整红线与文案模板见 `ct-base` `docs/02-security-model.md` §5。

## Menu / Navigation Design (ct-base §6)

### 7. Menu / Navigation Design — Non-Exclusive / 交互菜单 / 导航设计：互不互斥
- 全库通用 UX 基线。ct-registry 的注册库 / 场景入口**不得设计成互斥树**：同一注册库可出现在多个入口下。 / Library-wide UX baseline. The registry / scenario entries MUST NOT be a mutually-exclusive tree; the same source can appear under multiple top-level entries.
- 例：「德国试验」既可从「区域」入口勾 DRKS，也可从「全球全部源」入口勾 DRKS；「中国试验」既可从「区域」入口勾 CDE+ChiCTR，也可从「中国全覆盖」预设进入。 / Example: "German trials" is reachable BOTH from a **Region** entry (DRKS) AND from an **All global sources** entry (DRKS); "China trials" from both **Region** (CDE+ChiCTR) and an **China coverage** preset.
- 菜单是「引导」而非「严格分类」。 / The menu is a *navigation aid*, not a taxonomy.

### 7.1 Natural Language Dialogue / 自然语言对话参数确认
- 当用户通过自然语言触发检索时，遵循本技能 `references/search_menu.md` 定义的对话流程（ct-base §6.1 的定制实现）。 / When triggered via natural language, follow the dialogue flow defined in `references/search_menu.md` (the ct-registry customization of ct-base §6.1).
- 核心流程（2026-07-30 更新）：识别意图 → 收集参数 → **Gate1 检索前简报**（关键字/范围/时间窗/demand_id/免费10次每日）→ 执行 → **Gate2 列表确认**（先给列表，确认正确后再确认是否抓详情/下载）。参数缺失时最多追问 2 轮，然后使用默认值。 / Core flow (updated 2026-07-30): parse intent → collect params → **Gate1 pre-search brief** (keywords/scope/time-window/demand_id/free-10-per-day) → execute → **Gate2 list confirmation** (show list first, then confirm details/download after user approves the list). Max 2 rounds of follow-up for missing params, then use defaults.
- 定制要点：检索主题（cond/intr/drug）必填；数据源默认 CT.gov+EU CTR（Tier 1 直连）；国外源术语未命中触发确认门（§6.4）；详情抓取按条目数分档——≤100 条直接自动抓取，>100 条先确认列表再抓取；文档（PDF）始终需显式确认，不自动下载。 / Customization: search term required; default sources CT.gov+EU CTR; foreign-source term miss triggers a confirm gate (§6.4); detail fetching is tiered by count — ≤100 auto-fetch directly, >100 confirm list first; documents (PDF) always require explicit confirmation, never auto-download.

---

## Dependencies

### Python (shared + business)
```
requests>=2.28
pandas>=1.5
beautifulsoup4>=4.12
lxml>=4.9
# optional
matplotlib>=3.6     # PNG charts
playwright>=1.40    # CDE local scraping (requires playwright install chromium)
```
