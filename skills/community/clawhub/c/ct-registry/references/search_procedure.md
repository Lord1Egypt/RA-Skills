# Search procedure (three steps, force order)

Every search MUST execute in this order — no skipping, no reordering:

1. **Determine the source scope (scope first, then keywords).**
   - First confirm with the user/requirement which registries to cover. Options: CT.gov (direct),
     EU-CTR (direct), CDE (China, external workflow), WHO ICTRP (global mirror, external workflow),
     ChiCTR / ISRCTN / DRKS (external workflow, endpoints to be provisioned).
   - **Scope merge rule (key):** if the scope includes BOTH **WHO ICTRP + CDE**, they already
     **directly cover** the respective sites, so NO independent search of CT.gov / EU-CTR / ChiCTR /
     ISRCTN / DRKS is needed — WHO ICTRP mirrors these 14+ primary registries (incl. CT.gov, EU-CTR,
     ISRCTN, DRKS, ChiCTR) in one call; CDE independently covers China drug trials (WHO's English-title
     matching misses Chinese-registered trials, so CDE is ALWAYS searched independently).
     → "WHO + CDE" = "global + China" full coverage, actually hitting only **two endpoints**.
   - **⚠️ WHO and CDE MUST be invoked SEPARATELY — never one request for both libraries (user
     2026-07-28 correction):** although they share the same unified endpoint URL and the same token,
     each is an independent call — `search_ictrp.py --source who …` (call ①) +
     `search_ictrp.py --source chinadrugtrials …` (call ②). The shared endpoint quota is merged per
     demand (`demand_id`) and counted once — still two independent HTTP requests, only de-duplicated
     by the shared demand; `ct_registry.py` orchestrates them as two independent sub-flows — do NOT
     merge into a single HTTP request.
   - Only when WHO is unreachable (no token / 403) do you **fall back** to direct CT.gov / EU-CTR etc.
     (see `references/search_menu.md` FALLBACK-PROMPT flow; do NOT auto-fan-out).
   - Flags: `ct_registry.py` `--with-ictrp` / `--with-cde` / `--with-euctr` / `--with-chictr`
     / `--with-isrctn` / `--with-drks`; or call each `search_*.py` separately.

2. **Determine keywords per scope, with necessary zh/en translation.**
   - Pick terms per included registry by its language/matching habit:
     - **CT.gov / WHO ICTRP / PubChem (English sources):** use English terms (e.g. `Type 2 Diabetes` + `DPP-4 inhibitor`).
     - **CDE (Chinese library):** MUST translate to Chinese, and strip the class suffix "类".
       **DPP-4 inhibitor has no "DPP-4抑制剂" string in CDE** — all its drug names are "**列汀**" class
       (sitagliptin/saxagliptin/vildagliptin/linagliptin/alogliptin/trelagliptin/tegliptin/prugliatin…),
       so use **`drugs_name=列汀`** (substring match) to catch them all; do NOT use `DPP-4抑制剂`
       directly as a CDE keyword (=0 hits). Status uses **`trial_status=进行中`** (enum value, not "正在进行").
     - Category terms (e.g. a drug class) prefer **abbreviation/full-name or enum members**, not a bare class suffix
       (see `references/keyword_match.md` and 21 empirical probe lessons).
   - Chinese primary terms are auto-translated via `kw_localize.localize(text,"zh")`; an English source
     term not in the term table goes through the confirmation gate (never silently search a Chinese library with English).
   - **CDE search uses silent fallback (updated 2026-08-11):** the orchestrator first runs the Chinese keyword
     against CDE; if it returns 0 records AND a valid English translation exists, it automatically re-runs with
     the English keyword and merges the two result sets. This replaces the previous default bilingual parallel
     (which always fired both zh+en concurrently). Disable silent fallback with `--no-cde-bilingual`.

3. **Execute the search and return results.**
   - Direct sources (CT.gov / EU-CTR / PubChem): free, direct `--run`, not counted against the shared daily quota.
   - External-workflow sources (WHO / CDE / ChiCTR / ISRCTN / DRKS): via the shared endpoint, counted
     **once per demand (`demand_id`)** — WHO+CDE, keyword tweaks, and repeats within one demand all merge
     to 1, governed by the `usage_guard` daily cap of 1000 **demands** (blocks at cap). **Currently free**;
     the cap exists purely for fair shared-resource use — see README "配额与资源使用". **Token is
     localized, long-lived, no per-use re-sign** (only a rare 403 warrants `--store-token`).
   - **P4 async fire-and-forget (updated 2026-08-11):** the Coze `/run` endpoint returns immediately with
     a `run_id`; the client polls `/run/status/{run_id}` with exponential backoff. This bypasses the
     gateway's 300s hard wall. The workflow runs Playwright + Chromium headless shell for both CDE and
     WHO ICTRP (no remote API parsing), with a node-level budget of 270s per source. Detail mode uses
     8-thread parallel fetching.
   - After retrieval, uniformly `normalize → aggregate → report`:
     - **Excel is the final artifact (generated internally):** the orchestrator auto-calls
       `export_xlsx.export_workbook` at the end to produce `report.xlsx` (4 sheets); no hand-written
       temp script needed. Optional flags: `--no-excel` (off), `--lang {auto,zh,en}` (UI language),
       `--min-year N` (exact registration-year lower bound ≥N, with CDE year-from-reg-no fallback when
       year missing). Visual spec (navy palette / 24px header / zebra rows / status colour blocks /
       cover logo) comes from the **ct-base `excel_style` shared standard** (`export_xlsx.py` injects
       `../ct-base/scripts` via `sys.path` then `from excel_style import …`) — not redefined here.
     - **Intermediate files cleaned by default:** `report.md` and all `*.json` (incl. `normalized*.json`/
       `agg*.json`/source responses `ictrp.json`/`cde.json`) are deleted by default; **only `.xlsx` is kept**;
       add `--keep-meta` to retain debug intermediates.
     - The report includes a **fully clickable homepage link** per record (registration no. resolved to
       each registry's native URL); PDFs are NOT downloaded by default (only `--download-docs` with an
       explicit user request writes to disk).
   - **List first** (total/scope/samples + "list-mode phase/sponsor is Unknown" note); **detail by item
     count**: ≤100 fetched directly (auto), >100 confirm list first (see Agent interaction contract Gate 2);
     **PDFs NOT downloaded by default** (explicit user confirmation required to write to disk).

> These three steps are the skill contract: scope, then translation, then search. **Do NOT hard-code
> EN/ZH terms before scope is fixed**, and do NOT separately hit CT.gov/EU-CTR/ChiCTR/ISRCTN/DRKS when
> WHO+CDE already cover them.

# Keyword-System Confirmation Gate (v0.4)

When the user provides resolvable search terms, the skill **first proactively expands the keyword
system** (zh/en mutual translation + synonyms/aliases + drug-class enum, generated as a Manifest by
`ct-base/scripts/kw_localize.py: expand_keyword()`), **then FORCES a menu for the user to confirm/supplement**
— never `--run` before confirmation. This differs from the pre-search brief (Gate 1): Gate 1 allows
"skip if scope is clear", but **this gate is mandatory** — because the expanded terms are added by the
skill on the user's behalf and must be reviewed.

- **Expansion dimensions (core three):**
  1. zh/en mutual translation (reuse `localize` / `term_map` / `_EXTRA` / `_SYNONYMS` / brand↔generic);
  2. synonyms / aliases and brand↔generic (`_SYNONYMS` / `_BRAND_GENERIC`, **cover the whole therapeutic area at once**);
  3. drug-class enum (`_CLASS_MEMBERS` extended: 列汀/格列净/沙坦/他汀/替尼/磺脲/格列奈/格列酮/ACEI/β-blocker/mAb
     **enumerated by target family**).
- **Per-source dispatch:** the Manifest's `per_source` picks the best term set per source matching
  semantics (WHO/CT.gov exact vs CDE substring), and flags risk (rules from `references/keyword_match.md`,
  e.g. "列汀类=0").
- **Mandatory confirmation:** `render_kw_system_menu(manifest)` (multi-axis uses
  `render_kw_system_menu_multi`) renders a numbered menu (adopt / drop term / add term / adjust scope /
  cancel); only after the user picks "adopt" does it proceed to Gate 1 → search.
- **Session cache (confirmed 2026-07-31):** after the user first "adopts", the Manifest is cached to
  disk (`config/kw_system_cache.json`, md5-deduped); re-running the same terms in this session auto-adopts,
  no menu. Delete the cache file or change terms to re-confirm.
- **🔴 Non-interactive (agent) calls MUST pass one of `--no-expand` / `--kw-en` / `--kw-zh` / `--kw-adopt` (2026-08-13):** the gate renders a menu and calls `sys.exit(0)` when no skip flag and no session cache exists — it does NOT check whether stdin is a TTY and does NOT respect `--auto-confirm` (which only auto-accepts result-count confirmations, not this gate). An agent that copies the bare `--cond ... --run` recipe silently exits with zero output. Prefer `--no-expand` (simplest, fully deterministic); `--kw-en "<final term set>"` if you want the expanded/edited terms injected explicitly.
- **Skip / edit injection:** only when the user explicitly passes `--no-expand`, or after editing in the
  gate directly injects the final term set via `--kw-en` / `--kw-zh`, does the menu skip and go straight to
  Gate 1 (legacy behaviour preserved). `--expand-intent {disease,intervention,drug,drug_class}` can
  explicitly set intent to avoid auto-misjudgement; `--kw-adopt` means the user already picked "adopt" in the menu.
- **Implementation location:** `ct_registry.py: _kw_system_gate()` is inserted in `main()`'s `--run`
  branch, before building per-source commands; after confirmation it injects the `per_source` term set by
  reusing the existing override flags `--confirm-cond` / `--confirm-intr` / `--ictrp-keyword` / `--cde-keyword` / `--chictr-keyword`.
- **Lexicon fully externalized + migrated to ct-base (2026-07-31):** all expansion lexicons (synonyms/aliases,
  brand↔generic, drug-class members, mAb target families, mechanism aliases, class EN→ZH suffixes,
  `_EXTRA` translation safety net, drug-name EN→ZH) are moved to **`ct-base/scripts/kw_lexicon.json`**
  (single JSON, no in-code fallback). The keyword-expansion engine `kw_localize.py` (incl. loader) and
  `term_map.json` are also migrated to ct-base (`ct-base/scripts/` + `ct-base/references/`) as a
  library-wide standard — ct-registry imports ct-base via `sys.path` then `import kw_localize`, no vendored copy.
  To add/adjust lexicon, edit `ct-base/scripts/kw_lexicon.json` only — no code change.
- **Bilingual prompts (ct-base i18n, 2026-07-31):** menu framework labels (title/original/candidates/
  per-source/risk/inference/confirm-options) all use `ct-base/scripts/i18n.py` `_t("kw_gate.*")` — English
  by default, auto-switch to Chinese on a Chinese OS; **raw data values (drug names, Chinese class suffixes,
  user-entered terms) are NEVER translated**. `ct_registry.py`'s stop message also uses `_t("kw_gate.stopped")`.
- Full rules and Manifest schema: see `ct-base/references/keyword_expand.md` (library-wide standard).


## CDE en→zh Translation Confirmation Card (endpoint path · 0.5.02)

> **家族统一标准**：本节是 `ct-base/references/bilingual_retrieval.md` §5
> Translation Confirmation Gate 的 **ct-registry 实例**；分档规则、确认卡格式、
> 记录契约以 ct-base 标准为准（可调用模板 `ct-base/scripts/translation_gate.py`）。
> 下文仅保留 CDE 特有细则，与标准冲突时以标准为准。

> Scope: **unified-endpoint direct path** (`search_ictrp.py --source chinadrugtrials`, or the
> in-endpoint engine). The interactive `ct_registry.py` path is already covered by the
> Keyword-System Confirmation Gate above (Manifest `per_source.cde` zh terms are confirmed
> in that menu) — do NOT double-confirm there.

**Background (2026-11-11 field-tested):** CDE is a Chinese-language library — English keywords
return 0 hits (`keywords=奥希替尼` → 20 rows vs `keywords=osimertinib` → 0). The endpoint now
auto-translates pure-ASCII keywords via the en→zh reverse map (`_cde_drug_zh.json`, 501 entries,
fail-open). Because a machine translation can miss/mis-hit, the search result JSON carries a
`keyword_localization` array, and the dialogue layer MUST present a **translation confirmation
card** from it.

**Result JSON contract** (per keyword, inside `project_list`):

```json
"keyword_localization": [
  {"original": "osimertinib", "localized": "奥希替尼", "candidates": ["奥希替尼"],
   "mode": "whole", "ambiguous": false}
]
```

- `mode`: `whole` 整词命中 / `partial` 多词逐词映射 / `fail_open` 查无映射原样透传 / `native_zh` 本就是中文。
- `ambiguous: true` = 映射表存在多个中文候选，本次只取了首候选（可能漏检）。

**Dialogue-layer rules (mandatory):**

| 情形 | 动作 |
|---|---|
| `mode=native_zh`，或全部 `whole/partial` 且 `ambiguous=false` | **展示确认卡后直接继续**（知会即可，不阻断） |
| 任一 `ambiguous=true` | **必须停下确认**：列出全部候选让用户选（或另给词），确认后带 `--cde-keyword "<用户选的中文词>"` 重跑 |
| 任一 `mode=fail_open` 且 `original` 为 ASCII | **必须停下询问**：该英文词未翻译，在 CDE 必然 0 命中——请用户提供中文通用名/商品名，或明确确认「仅用其余词检索」 |

**确认卡格式**（对话与工作台统一使用此 markdown 表）:

```markdown
### 🔤 CDE 关键词翻译确认
| 原词 | 中文检索词 | 候选 | 状态 |
|---|---|---|---|
| osimertinib | 奥希替尼 | 奥希替尼 | ✅ 已应用 |
| SGB-9768 | SGB-9768 | — | ⚠️ 未翻译（CDE 0 命中风险，请给中文名） |

请确认或改词后我再重跑 CDE 检索（回车=按上表继续）。
```

- 展示时机：CDE 检索**返回后**随结果一起展示（翻译在端点内自动发生，前置确认只在
  `ambiguous/fail_open` 时通过重跑体现）；若用户在 Gate 菜单阶段就想预览映射，可用
  `--kw-zh` 直接注入已确认中文词集，端点不再触发自动翻译注入差异。
- 翻译词表来源：`ct-registry/references/drug_name_map.json`（zh→en 正向）反向索引生成于
  `src/graphs/nodes/_cde_drug_zh.json`；补词请编辑正向表后重新生成反查表。
