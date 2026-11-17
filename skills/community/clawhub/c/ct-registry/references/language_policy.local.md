# Language Policy / 双语语言策略（ct-registry 专属补充）

> **通用双语策略以 ct-base 为单一事实来源（Single Source of Truth）**：本文件只保留 ct-registry 的专属增补，
> 通用条款（三条核心规则、中文环境检测、内容级检测、coze `locale`/`user_language` 规则、文档语言约定、
> 分隔符规范、locale 链式传播等）见 `references/language_policy.md`（真源 `ct-base/references/language_policy.md`）。
>
> Runtime prompts（面向用户的运行时提示）统一走 ct-base 共享 `i18n`（EN 默认、`zh-*` 环境自动切中文）；本技能**已删除**本地 `scripts/i18n.py` 副本（与 ct-base 逐字重复、无任何脚本导入，属死代码），不再保留。

## Search-keyword localization (ct-registry) / 检索关键字本地化

> **Distinct from the message i18n above.** This covers auto-switching the user's *search
> keyword* between Chinese and English per target registry — not UI text.

- **Problem**: a user types ONE keyword (e.g. `--cond "非小细胞肺癌"`); foreign registries
  (CT.gov, EU CTR, ISRCTN, DRKS) expect **ENGLISH**, domestic China sources (CDE, ChiCTR)
  expect **CHINESE** (and also accept ENGLISH).
- **Mechanism**: `ct-base/scripts/kw_localize.py` + `ct-base/references/term_map.json` (curated offline ZH↔EN
  term map, **no translation API call**). `ct_registry.py` calls `kl.localize(text, target_lang)`
  before dispatching to each source.
- **Two-phase resolution / 两阶段解析**:
  1. **Terminology first / 术语优先**: every switch first consults `ct-base/references/term_map.json`
     (~190 curated ZH↔EN terms) and the embedded `_EXTRA` fallback in `ct-base/scripts/kw_localize.py`.
     A hit is trusted and used directly. / 先查术语表与 `_EXTRA` 兜底，命中即用。
  2. **Confirm-on-miss (foreign sources) / 未命中需确认（仅国外源）**: if a **CT.gov / PubChem**
     keyword is NOT in the map and is in the wrong language, `ct_registry.py` **stops** and prints
     a suggested English translation — it never silently searches CT.gov with Chinese (which would
     quietly miss hits). The agent proposes the translation, asks the user to confirm, then re-runs
     with `--confirm-cond` / `--confirm-intr` / `--confirm-drug` (or rewrites the arg in English).
     `--auto-confirm` skips the gate (use only for known-safe automation). / 若 CT.gov/PubChem
     关键字不在表且语种不对，运行**中止**并打印建议英文译文，绝不用中文静默搜 CT.gov；
     确认后通过 `--confirm-*` 或改写参数为英文重跑。`--auto-confirm` 跳过确认门。
- **CDE silent fallback (updated 2026-08-11) / CDE 静默降级（2026-08-11 更新）**: CDE accepts both Chinese and
  English. When a CDE keyword has a known (zh, en) pair, `ct_registry.py` first searches CDE **in Chinese
  only**. If the Chinese search returns 0 records AND a valid English translation exists, it **automatically
  re-runs with the English keyword** and merges the two result sets (dedup by `registry_id`). This replaces
  the previous default bilingual parallel (which always fired both zh+en concurrently), cutting HTTP calls
  roughly in half while covering trials registered in either language on CDE. Disable with
  `--no-cde-bilingual`. / CDE 同时接受中英文；可派生 (zh,en) 对时，技能先用中文检索 CDE；若中文返回 0 条且
  存在有效英文译文，则**自动用英文再查一次**并合并去重。这取代了此前默认的中英并行双检（总是同时发两个 HTTP），
  在覆盖任一种语言登记试验的前提下，HTTP 调用数约减半。如需关闭用 `--no-cde-bilingual`。
- **Behavior**:
  - Input already in the target language → used as-is (no-op).
  - Term found in map → translated; a `[ct_registry][i18n]` log line documents the switch.
  - Foreign-source term NOT in map → confirm gate (`[CONFIRM]` + `[ABORT]`, exit 2) before any
    network call (see above). CDE-source miss → logged (`[CONFIRM][CDE]`) but still searched.
  - Extend `ct-base/references/term_map.json` / `_EXTRA` to broaden coverage.
- **Override**: explicit per-source args (`--cde-keyword`, `--confirm-*`) always win over
  auto-derived. / 显式参数（`--cde-keyword`、`--confirm-*`）始终优先于自动派生。
