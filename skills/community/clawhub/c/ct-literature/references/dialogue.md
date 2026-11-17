# Dialogue Protocol & Bug Reporting (ct-literature)

> Extracted verbatim from `SKILL.md` (2026-09-27, line-budget refactor — SKILL.md ≤ 200 lines per ct-base §16.1 / F02). No content removed; SKILL.md keeps the red-line summary and points here. Load this file when executing an NL dialogue round (triage / continuity / echo) or handling bug reports.

## Natural-Language Dialogue — Triage-First (mandatory)

NL dialogue MUST triage before choosing the interaction shape. Mandatory per
§6.2 + `search_menu.md` — this step is never skipped.

### Step 0 Triage (four buckets, run on the user's first message)

| Bucket | Condition | Behavior |
|---|---|---|
| **Simple** | topic + ≥2 parameters clear (e.g. "osimertinib systematic reviews since 2020") | straight to §4.2 preview confirmation; no §4.1 menu |
| **Complex** | topic given but parameters missing / multiple intents (e.g. "diabetes treatment literature") | §4.1 initial confirmation menu → once parameters are complete, forced through the §12 keyword gate → §4.2 preview confirmation → run |
| **Vague** | what the user wants is unclear (e.g. "find me that new drug") | grill-me branch questions (≤2 rounds), then re-triage |
| **Middle** | single deep point (e.g. "how to compute sample size") | answer directly; no menu |

### Red lines

- **Never skip triage and run `--run` directly.** Even with a clear topic, missing key parameters (review_type / year / sources / …) makes the Complex menu flow mandatory.
- **Never decide for the user.** The Complex menu must carry a "still unsure → explain the differences" entry (option ③ in the CN UI: 说「详细解释这些选择之间的差异」，我先讲清临床与统计含义再让你决定).
- **The §12 keyword-system confirmation gate is mandatory:** whenever the user provides parseable search terms, build the Manifest and let the user review the expanded keywords before running.

### Cross-turn continuity (continuity.md mode A, high risk)

ct-literature's query spec lives ONLY in the conversation thread (OpenAlex /
Europe PMC etc. are stateless remotes); a dropped field silently searches the
wrong scope.

#### Echo block (append after every run)

```
## 当前检索设定：topic=… | type=… | year=… | safety=… | depth=… | concepts=… | sources=… | max=… | verify=…
```

- Fixed prefix `## 当前检索设定：` (inherited by search_menu.md §13)
- Fields are `key=value`, pipe-separated; missing defaults use `—`; **never omit fields**
- Full field list: `topic / type / year / safety / depth / concepts / sources / max / verify`

#### Follow-ups change only the changed fields

The LLM must read the MOST RECENT settings block in the conversation, override
only the fields the user changed this turn, keep the rest as-is, then proceed
to the §12 gate or run.

#### merge_spec fallback (default path)

ct-literature is a high-risk skill (continuity.md §5.1); `merge_spec.py` is the
DEFAULT path on follow-ups:

```bash
echo '{"prev":{previous full spec},"cur":{this-turn partial}}' \
  | python scripts/merge_spec.py
```

Feed the `merged` output into the §12 keyword gate. `prev` comes from the
thread's latest settings block — never persisted, never cached across turns.

#### Local-only continuity

OpenAlex / Europe PMC / bioRxiv / medRxiv are all **stateless remotes** — they
do not remember your previous search parameters. Continuity (parameter
inheritance) MUST be solved locally (thread-resident + echo block +
merge_spec); there is no "the remote will remember" fallback.

### Execution flow

```
user request → Step 0 Triage
  ├─ Simple → §4.2 preview confirm → §12 keyword gate → run → §13 echo
  ├─ Complex → §4.1 initial menu → parameters complete → §12 keyword gate → §4.2 preview confirm → run → §13 echo
  ├─ Vague → grill-me (≤2 rounds) → re-triage
  └─ Middle → answer directly (no menu)
```

### Citation-Expand & 引导式剧本 (B.2 / C)

- **Citation-Expand（种子驱动 snowball）**：用户以某篇具体论文（DOI / PMID / OpenAlex ID / 题名）为起点要求追溯其引用/被引时，进入 §14 子意图——**不依赖主题检索结果**，直接解析种子为 OpenAlex work ID 并扩展 1-hop 引文网络。CLI：`--snowball-seed "<种子>" [--snowball-direction references|cited_by|both]`。解析失败如实回报，绝不编造。
- **引导式检索剧本（读→扩→链）**：把 `--download-pdf --anchor` + `--depth` + snowball 拼成分段节奏。CLI：`--guided` 一次性开启 PDF 段落级下载与标准深度；预览确认菜单见 `search_menu.md` §4.2 选项 ④。默认关，避免打扰简单查询。

> 红线：种子驱动文献同样过反幻觉引用验证与去重；未核验的相关性裁决只作排序/提示，不构成最终纳入/排除（呼应接缝护栏）。

## Bug Reporting (§20.3, adapter: `adapters/bug_report.py`)

- **Trigger:** (A) explicit user request ("report a bug" / "反馈问题" / "提交错误报告") → straight to two-stage confirmation, unlimited per session; (B) strong signal (unexpected non-zero exit / engine or compute error / user explicitly questions the result) **and** the same operation was retried ≥1 → at most 1 unsolicited proposal/session.
- **Two-stage confirmation (2026-08-21):** ① propose-with-preview — bilingual `confirm_prompt` together with the full sanitized report (invite a problem description; re-render before consent) → ② on explicit consent, `send_to_endpoint` (auto action=report, endpoint `https://ct-bugreport.coze.site/run`, token = §5 public credential). Decline → never re-propose this session.
- **Sanitization is hard:** 11-key whitelist only (skill / version / error_type / error_code / engine_status / description / locale / query_origin / session_hash / attempts / test) — never raw data or subject records; `description` is the single user-reviewed free-text field. No cloud call → `save_local_report()` (local md + author email).
- **Client-only:** sends `report` only; governance actions belong to `ct-update` (author side). Post-send (2026-08-22): endpoint returns `history` → reply via `confirm_thanks` + `build_followup` (bilingual, locale-switched).

Invoke: `python adapters/bug_report.py --error-type <t> --description "<free text>" [--send]` (add `--send` only after the user confirms).
