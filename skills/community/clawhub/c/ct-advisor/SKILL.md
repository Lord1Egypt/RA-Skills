---
slug: ct-advisor
name: ct-advisor
displayName: Clinical Trial Chief Advisor / 临床试验总顾问
cn_name: 临床试验总顾问
version: 1.3.42
invocable: true
required_commands: [python]
summary: "面向临床研发全生命周期的 ct 系列「总入口」，云端辅助的临床试验总顾问。覆盖范围已扩大至合规应答 / 项目运营 / 交付物撰写 / 方案设计 / 统计分析 / 注册申报 / 安全性 / 数据管理 / 真实世界研究——仅当明确非医药/生命科学语境时才给建设性转介建议。本地侧在确定性二值闸门（是否 vague）与附件解码之外，新增会话上下文注入（多轮承接）；答案缓存与去重一律由云端承担（仅为独立问题服务，本地不缓存答案）；不保留知识库，不进行本地网络检索。外部参考：teal 临床数据交互探索框架。"
description: "The single entry point for the ct-series across the full clinical-development lifecycle — a cloud-assisted clinical trial advisor. Coverage has been broadened to regulatory-response / trial-operations / deliverable-drafting / study-design / statistics / submission / safety / data-management / real-world-evidence; only clearly non-medical / non-life-science questions receive a constructive referral. On the local side, in addition to the deterministic vague-gate and attachment decoding, it injects multi-turn session context (continuation of prior rounds); answer caching and deduplication are handled entirely in the cloud (serving standalone questions only — no answer cache is kept locally); no knowledge base is retained locally and no local network retrieval occurs. External reference: the teal clinical-data interactive exploration framework. / 面向临床研发全生命周期的 ct 系列「总入口」，云端辅助的临床试验总顾问。覆盖范围已扩大至合规应答 / 项目运营 / 交付物撰写 / 方案设计 / 统计分析 / 注册申报 / 安全性 / 数据管理 / 真实世界研究——仅当明确非医药/生命科学语境时才给建设性转介建议。本地侧在确定性二值闸门（是否 vague）与附件解码之外，新增会话上下文注入（多轮承接）；答案缓存与去重一律由云端承担（仅为独立问题服务，本地不缓存答案）；不保留知识库，不进行本地网络检索。外部参考：teal 临床数据交互探索框架。"
license: MIT
triggers:
  - "ct-advisor"
  - "clinical trial advisor"
  - "ct advisor"
  - "trial methodology"
  - "clinical trial methodology"
  - "clinical research advisor"
  - "trial design"
  - "GCP question"
  - "临床试验顾问"
  - "临床试验总顾问"
trigger_scope: "触发词覆盖临床试验方法学/法规/设计/合规应答/项目运营/交付物撰写/QC/安全性/数据/注册/情报类问题；尽量扩大适用范围，仅对明确非医药/生命科学语境的问题（如消费电子、金融、快消、地产等）给出建设性转介建议，绝不空拒；不含文件系统写入与系统级 API 调用。"
metadata:
  openclaw: { emoji: "🛠️", icon: "assets/icon.svg" }
  authors: ["medstatstar", "phoe-zip"]
  family: ct-series
  homepage: "https://github.com/medstatstar/ct-advisor"
permissions:
  scope: "user-space-only"
  network: "controlled-coze-opt-in"
  network_note: "All questions are forwarded to Coze (single call, internal `scripts/orchestrate.py`). Local side performs NO knowledge base lookup, NO local network retrieval, NO web search. Attachments under 5 MB are uploaded as original bytes to Coze `/upload_file` and shipped as the top-level `doc_context` field (Coze decodes natively); attachments over 5 MB are converted to Markdown locally via `scripts/office_to_md.py` (stdlib-only) and the resulting .md is uploaded through the SAME doc_context channel. The Coze-side knowledge base is the single source of truth."
  filesystem: "Read-only to own files; no confidential data leaves locally — Coze payloads sanitized, query_origin is a stable per-machine sha256 hash (non-PII)."
adapted_from: "https://github.com/A-xin946/clinical-trial-advisor"
dependencies:
  - {slug: ct-registry,   tier: A}
  - {slug: ct-safety,     tier: A}
  - {slug: ct-literature, tier: A}
  - {slug: ct-samplesize, tier: A}
tier: A
---
## Data Egress Guardrail (CT family standard · F33)

This skill may call external endpoints (Coze services, shared third-party search
endpoints, public APIs or LLMs). **Internal confidential data must not leave the
local domain.** Mandatory rules:

- **Never outbound**: patient-level records, unpublished protocols / CSRs / internal
  documents, personal identifiers or sponsor-confidential content — as query terms,
  attachments or prompt payload.
- **Allowed minimum**: public search terms and non-content metadata only (machine
  hash, skill version, entry point, language, request id). Results from public
  registries (ct.gov / CDE / FAERS / OpenAlex / PubMed, etc.) are processed locally.
- **Local first**: computation, de-identification, aggregation and reporting stay on
  this machine; confirm the payload carries no confidential field before any cloud call.
- **Visible disclosure**: workbench search forms must state the outbound endpoint and
  this boundary in visible text, not only in a hover tooltip.
- **Fail loud**: stop and tell the user if any rule cannot be guaranteed; never
  degrade silently.

Machine-checked by `ct-base/scripts/spec_lint.py` rule **F33**.


# Clinical Trial Chief Advisor

## Language

- **English guide** → [README.md](https://github.com/medstatstar/ct-advisor/blob/main/README.md) · **中文指南** → [README_zh-CN.md](https://github.com/medstatstar/ct-advisor/blob/main/README_zh-CN.md)
- **This SKILL.md body is English-only, agent-facing.** Bilingual walkthroughs live in the two READMEs; the answer language follows the user's question language.

## 🔴 HIGHEST PRIORITY: scripts/entry.py is the ONLY permitted action

> **The local LLM is FORBIDDEN from making any decisions in this skill. Its ONE AND ONLY allowed action is:** Run the single entry point with the user's question (and optional attachment). Pipe the stdout to the user verbatim. CLI details live in `references/ADVANCED.md` — do not type commands from here.
>
> Since **v1.3.21** the stdout is **plain text followed by a trailing integrity line** and one
> ASCII pointer to the answer file — no decoding, no transcription, no second command:
>
> ```
> {the answer text, as many lines as it needs}
> <<<CT_ANSWER_END>>>
> checksum: {sha256[:16]}
> answer_file: C:/Users/<user>/.workbuddy/skills/ct-advisor/_answers/{checksum}.md
> ```
>
> **One entry point, one output shape, one protocol, one place where the protocol is produced.**
> Since v1.3.21 there is **no base64 anywhere in the pipeline** — not between code modules, not
> on the wire, not in the browser. The reason is historical: v1.3.9 introduced base64 to survive
> cp936 console mojibake, but that forced the LLM to hand-copy a ~2.6k-char random string into a
> second command (2026-10-16 incident: `5Lzd` typed for `5L+d`, a "checksum failure" that was
> pure transcription damage, then three real Coze calls for one question). The wrapper that fixed
> it left two parallel protocols, a 4× payload inflation, and — once the browser started taking
> the API directly — a decoder in *each* client. v1.3.21 removes the need instead of managing it:
> **encoding is no longer a decision made at the exit**. `entry.py` writes UTF-8 bytes straight to
> `stdout.buffer` (constant, no code-page inspection, no flags), the marker/checksum pair is
> produced in exactly one function, and the same bytes are also on disk. `scripts/ask.py` survives
> only as a zero-logic forwarding shim for stale callers.

**HARD GATE — the following are absolutely PROHIBITED for the local LLM:**
- ❌ **NEVER** read, search, or reference any local knowledge base (the `knowledge/` directory has been removed)
- ❌ **NEVER** perform any local network retrieval or web search (`references/search-sites.md` has been removed)
- ❌ **NEVER** answer the question from the LLM's own knowledge — all domain expertise lives on the Coze side
- ❌ **NEVER** bypass `entry.py` by calling `route.py`, `refine_answer.py`, `orchestrate.py`, or any other script directly
- ❌ **NEVER** rewrite, rephrase, reorder, summarize, or "polish" the answer text that precedes `<<<CT_ANSWER_END>>>`
- ❌ **NEVER** append a summary, lead-in, closing remark, or "key takeaways" before or after the answer
- ❌ **NEVER** strip, alter, or re-generate the `<<<CT_ANSWER_END>>>` marker or the `checksum:` line that follows it
- ❌ **NEVER** translate or align language (the code already handles that)
- ❌ **NEVER** inject process narration ("Step 2", "Coze returned", "assembling payload")
- ❌ **NEVER** decide whether to forward to Coze — ALL questions are forwarded (entry.py handles routing internally)
- ❌ **NEVER** wrap, encode, base64-ify, or otherwise re-transport the answer on your own — the pipeline already emits the final form
- ❌ **NEVER** present the `answer_file:` line as part of the answer (it is a pointer, not content)
- ❌ **NEVER** discard stderr with `2>$null` / `2>/dev/null` — stderr carries the answer-cache-hit / resident-service / `[ct-advisor][ERR]` signals that tell you whether a Coze call actually happened

**Why this rule exists:** The local LLM's "helpful" instincts (answering from its own knowledge, pre-reading files, post-formatting answers) have repeatedly violated the pipeline contract, destroyed Coze-delivered content formatting, altered numeric precision, injected unsolicited content, and bypassed the cloud analysis entirely. This rule eliminates ALL local LLM decision space.

> **`--stitch` is the sole non-forwarding mode.** It consumes skill outputs that
> already exist (no question is being answered, so no Coze call happens). It is
> still `entry.py`, still zero-LLM, still the one permitted action — see the
> Return path section below.

## How to use this skill

Run the single entry point with the user's question. Optionally attach a file (e.g. a CSR or protocol snippet). The stdout is the final answer — deliver it verbatim.

CLI invocation details, examples, and flag notes → `references/ADVANCED.md`.

### Return path: `entry.py --stitch` (2026-11-09)

Handoff used to be one-way: after the user ran several sibling skills there was no
code-driven way back. `--stitch` closes that loop **without adding a second entry
point or giving the local LLM any decision space**:

```
python scripts/entry.py --stitch '{"question":"...","results":[
  {"tool":"ct-registry","files":["<path>/report.md"]},
  {"tool":"ct-safety","files":["<path>/faers_report.xlsx"]}]}'
python scripts/entry.py --stitch @spec.json     # --q may be omitted in stitch mode
```

`scripts/stitch_results.py` parses `.md/.txt/.log/.json/.csv/.tsv/.xlsx` locally
(stdlib only) and stitches a deterministic summary through the **same**
`_emit_plain` exit (marker / checksum / answer_file). **By default** it never
imports the orchestrator or any HTTP client, never calls Coze, and never sends
skill outputs anywhere — 🔴 F33: outputs may contain Tier-B confidential material,
so the whole path stays on this machine. Reads are bounded by an extension allowlist, a 2 MB
per-file cap, a 20-file cap, a 4 000-char excerpt cap and a credential-filename
denylist. Missing or unparsable outputs are reported, never invented. The summary
is explicitly marked non-audit-grade and never rewrites or infers numbers.

🔴 **HARD GATE unchanged**: `--stitch` is a mode of `entry.py`, not another script
the agent may choose. The agent still runs one command and pipes stdout verbatim;
the handoff answer itself carries the ready-to-use `--stitch` hint, generated in
code by `refine_answer._stitch_hint()`.

**L3 methodology interpretation (opt-in, 2026-11-09)**: adding
`"interpret": true` to the stitch spec asks for a methodology explanation of the
results. `scripts/interpret_results.py` — a **separate** module, so
`stitch_results.py` stays statically free of any network import — sends **only**
a code-built methodology question plus allowlisted **sanitized numeric values**
(max 12 finite numbers, from JSON outputs only) to the pre-authorized Coze
endpoint. The user's original question, raw output text, file names/paths, drug /
protocol names, trial IDs and subject data **never leave the machine** (F33).
The outbound request additionally passes the explicit
`_check_outbound_authorization` gate; if the endpoint is not whitelisted, no
allowlisted numbers exist, or Coze returns an error / `need_tool` / an empty
answer, the cloud interpretation is discarded and only the local summary is
delivered, with the reason stated. Covered by
`scripts/test_interpret_sanitization.py` (27 offline cases).

> **There are no flags to tune the output.** `--out`, `--b64`, `--answer-file` and
> `--no-answer-file` were removed in v1.3.21: every run writes the same bytes to stdout and the
> same bytes to `<skill>/_answers/{checksum}.md`. That file is the **data source of truth** — if
> a terminal shows mojibake (a display-layer problem, never a data problem), read that file and
> deliver from it instead of re-running anything.
>
> **Length is no longer a channel risk.** A 6000-char CJK answer now leaves `entry.py` as
> ≈6,000 characters. Under base64 it was 24,000 — past the PowerShell ~20,000 truncation line
> and hard against the Bash inline ceiling (~30,000 → persisted to a file with a 2 KB preview
> only). Decision table 1c covers the truncation signal.
>
> `scripts/ask.py` still exists but is **not** the entry point: it is a zero-logic forwarder
> that inherits `entry.py`'s stdout/stderr/exit code for stale callers.

### What entry.py does internally (all code, zero LLM) — the canonical pipeline

```
STEP 1  Attachment gate (if --attach) — BOTH paths ship a FILE via doc_context
        ├─ < 5 MB   → doc_memory.build_file_payload(allow_upload=True): upload ORIGINAL file to Coze /upload_file, ship as `doc_context` (mode=file_id; base64-forward fallback on failure)
        └─ > 5 MB   → convert locally (office_to_md.py for OOXML / direct read for txt-like), upload the resulting **.md** through the SAME doc_context channel + ℹ️ notice that cloud answers from the md version
STEP 2  Vague gate (deterministic regex, scripts/route.py — binary: vague | forwarded, the ONLY local gate): vague → clarify_loop.py (≤3 rounds) → questions to user, stop; forwarded → continue (Coze re-judges difficulty with its own LLM; timeout tier via route.timeout_tier)
STEP 3  Forward to Coze — orchestrate.run_orchestrate(payload): Coze async submit (/async_run, ms-level → task_id) + local prefetch (handoff card by default; brief only when explicitly enabled) → poll /task/{id} until terminal → merge (sync /run only as fallback when the async endpoint is unavailable)
STEP 4  Delegate stitch — if Coze returns <<<CT_TOOL_DELEGATE>>>, entry.py auto-runs refine_answer.py --card-inline (code, no LLM); since 2026-11-09 this normally emits a client handoff card (@skill:<slug>) instead of executing the sibling CLI
STEP 5  Output — entry.py writes the answer file (UTF-8), then the same bytes + `<<<CT_ANSWER_END>>>` + `checksum:` + `answer_file:` to stdout.buffer (single protocol, single producer since v1.3.21)
```

> **LLM-forbidden zone**: every STEP above is executed by code. The local LLM
> never picks the channel, never judges difficulty, never decides forwarding.

### Output format

`scripts/entry.py` — stdout is the **plain-text answer plus a trailing integrity line and an
ASCII pointer to the answer file**:

```
{the answer text, as many lines as it needs}
<<<CT_ANSWER_END>>>
checksum: {sha256[:16] of everything before the marker, LF-normalized}
answer_file: C:/Users/<user>/.workbuddy/skills/ct-advisor/_answers/{checksum}.md
```

The marker sits at the **end** on purpose: any channel truncation removes it together with
the checksum, so a damaged capture is obvious at a glance instead of silently passing. The
checksum covers the answer body only (everything from the first byte up to and including the
newline immediately before the marker), so it is trivially reproducible.

`answer_file` is an **absolute ASCII path**, so you can hand it straight to the file-read tool
with no path assembly. The absolute form is used only when it is pure ASCII; if the skill lives
under a CJK path (user name / directory), the value degrades to the relative `_answers/{sha16}.md`
instead — that is the one form guaranteed readable in a garbled console, and you then join it with
the skill root you already know. Either way the file holds **byte-identical** content to the
stdout body.

> **Where base64 no longer lives (v1.3.21)**: nowhere. `orchestrate._finalize`,
> `refine_answer._emit_plain` and `serve./ask` all pass **plain text**; the marker/checksum pair
> is produced in exactly one function (`entry._emit_plain`). If you ever see a base64 envelope in
> any output, it is a leftover from an old resident process — the code fingerprint makes
> `entry.py` restart it automatically, so just re-run once and report it.

### 🔴 Integrity check (HARD GATE · simplified in v1.3.19, final in v1.3.21)

Because the answer arrives as **plain text**, the whole check collapsed into one structural
question: **is the trailing `<<<CT_ANSWER_END>>>` marker there?**

| # | Observation | Meaning | Action |
|---|---|---|---|
| 1 | Marker + `checksum:` present, body non-empty | Capture complete | Deliver the body verbatim (`answer_file:` line included, it is not part of the answer). `checksum:` re-verification is optional here — the marker's presence already proves the capture was not cut. |
| 2 | Marker absent, or `checksum:` line missing | The tool channel truncated the capture | Re-capture the **same** command with Bash / Git Bash. **Do NOT re-run Coze.** |
| 3 | Marker present but checksum mismatch (code below) | Real corruption, not truncation | Do NOT deliver. Report expected vs actual and stop — never loop re-runs. |
| 4 | Body looks garbled but marker + checksum are intact | Display-layer code page, data intact | **Read the `answer_file:` path exactly as printed** (absolute ASCII — verified to survive the capture that destroyed the body) and deliver everything before `<<<CT_ANSWER_END>>>`. No re-run. **If that line is missing** (both candidate dirs unwritable), stop and report — never decode or guess the text. |

Re-running without capture evidence is a protocol violation: in the 2026-10-15/16 incidents it
made one question fire 2–3 times, dragging a single Q&A to minutes.

Verification code — only needed for a suspected mismatch in row 3:

```python
import hashlib, re
stdout = "...(entry.py output)..."
MARK = "<<<CT_ANSWER_END>>>"
if MARK in stdout:
    body = stdout.split(MARK, 1)[0]                    # everything before the marker
    expected = re.search(r"checksum:\s*([0-9a-f]{16})", stdout).group(1)
    if hashlib.sha256(body.encode("utf-8")).hexdigest()[:16] != expected:
        print("⚠️ answer integrity check failed")      # do not deliver, do not re-run
    else:
        print(body)                                    # deliver verbatim
```

**If the checksum does not match, the local LLM MUST NOT deliver the answer to the user.** This prevents any silent tampering.

> 🔴 **Encoding is no longer a setting you can get wrong (v1.3.21)**: `entry.py` writes the
> payload with `sys.stdout.buffer.write(utf-8 bytes)` — a **constant**, not a negotiation. It does
> not look at `sys.stdout.encoding`, `PYTHONIOENCODING`, or the console code page, and there is no
> flag to change it. Verified under `PYTHONIOENCODING=cp936`: the captured bytes decode as valid
> UTF-8 every time.
>
> What is *not* solved by that, and cannot be: a **terminal** may still render UTF-8 bytes through
> its own code page (`鏈熶复…`). That is a display-layer problem, so the engine does not try to
> detect it — instead every run also writes the identical bytes to
> `<skill>/_answers/{checksum}.md` and prints an **absolute ASCII** `answer_file:` line.
>
> 🔴 **The sanctioned repair is "read the source file", NOT "decode the garbled text"**: if stdout
> looks garbled, do exactly this —
>
> 1. take the path from the `answer_file:` line **as printed**. It is pure ASCII, so it survives the
>    very code page that mangled the answer (verified: in a simulated cp936 capture the whole answer
>    body was destroyed while this line came through byte-intact);
> 2. open it with the file-read tool — file reads are UTF-8 by default and independent of the
>    console code page;
> 3. deliver everything **before** `<<<CT_ANSWER_END>>>` verbatim.
>
> This is **not** a model "fixing" the text. The file never travelled through the console, so its
> bytes are the original ones; the model only moves bytes it did not author — precisely the role
> the HARD GATE allows. That is why reading the file works where every decode attempt fails.
> If `_answers/` is unwritable (network-share ACL refuses overwrite) the engine reuses an identical
> existing file instead of rewriting it, and falls back to `%TEMP%/ct-advisor/{checksum}.md` — the
> `answer_file:` value stays absolute, so the same three steps apply unchanged.
>
> 🔴 **No decoding of the garbled STRING — by anyone (HARD GATE · 2026-10-22)**: "read the file"
> above and "decode the mojibake" are different acts; **only the first is permitted**. Never ask the
> host model to repair / restore / guess echoed garbled text — not you, not a sub-agent, not any
> local model. This is not a capability gap, it is information loss. A cp936
> console is **not** a reversible double-encoding: many UTF-8 bytes are illegal under GBK, so the
> console substitutes `U+FFFD` and the original bytes are gone. Measured on a 127-char / 330-byte
> CJK answer: 13 `U+FFFD` substitutions, every repair chain (`cp936` / `gb18030` / `cp1252` /
> `latin-1` re-encode → UTF-8 decode) failed — even the `checksum:` line could not be recovered.
> Any "repaired" text you produce is invention: unverifiable against the checksum, and a
> rewrite of a clinical answer, which violates ALCOA+ and the HARD GATE. The **only** sanctioned
> recovery is reading `answer_file`; if that file does not exist, report the capture failure and
> stop — never deliver guessed text. (Latin-1 style 1:1 mis-decoding *is* reversible in theory,
> but the verdict is still "read the file", because the file is both cheaper and provably exact.)
>
> Optional hygiene, not a requirement: `[Console]::OutputEncoding = [Text.Encoding]::UTF8` before a
> PowerShell invocation makes the *screen* readable too. Note `$OutputEncoding` is a **different**
> variable (it governs stdin sent to native programs) and setting it alone does nothing; and the
> setting is per-process, so it must be applied in the same shell invocation.


> 🔴 **No host-model fallback (HARD GATE · 2026-10-15)**: ct-advisor is coze-only **by design** — there is no local knowledge base or database, so a host-model direct answer on a clinical question has no domain substrate and is **forbidden as a fallback** (a bare host-model answer was evaluated and rejected: quality cannot be guaranteed without the cloud knowledge base and tool chain). The same tiering rule means attachment / `doc_context` content must **never** leave the Coze channel. The ONLY sanctioned recovery for a broken capture is: **repair the capture → re-send once (≤1, usually served by the local cache)**. Everything else stops and reports.

> 🔴 **Short-circuit output obeys the same contract (2026-10-15 · unified into `session_store.py` 2026-10-22)**: both short-circuit paths — `session_store.cache_get` (exact-fingerprint answer cache, cross-session) and `session_store.dedup_check` (near-duplicate within a session window) — are wired into **both** the `entry.py` main chain AND the workbench `ct-advisor-proxy.py` (`/run` / `/async_run`). A short-circuited answer leaves `entry.py` through the **same plain-text exit** as a fresh Coze call (stderr marks `answer-cache hit` / `dedup short-circuit`; the proxy returns a local pseudo-task so the front-end is oblivious). A cached answer is a legitimate delivery, not an error.

> 🔴 **Single-run discipline (performance · as mandatory as the HARD GATE)**: `entry.py` is one complete Coze remote call and the main time cost of a single Q&A. The default is **one call per question**. **Re-calling `entry.py` purely to "verify" the output is strictly forbidden** — with the plain-text exit there is nothing left to verify locally. The single exception is decision-table row 2: **at most one re-send to repair a broken CAPTURE**, with the reason stated to the user — never for a checksum mismatch on clean text (row 3 → stop) and never without capture evidence. If you need to persist output, it is already on disk at `answer_file` — do not re-run for that either.

**Verification discipline (L3 · 2026-10-22, final in v1.3.21)**: the sha256 check is only needed on a suspected mismatch — the trailing marker already proves completeness in the normal path, and no flag can toggle the output shape any more. **Forbidden**: writing stdout to a temp file for the check, extra tool round-trips, post-hoc temp-file cleanup, and any attempt by the LLM to re-encode or re-transport the answer.

## Performance Optimization & Deployment Notes (L1/L2/L3, 2026-09-26)

This skill has implemented four performance optimizations; see `PERF_SOP.md` for details:
- **L1 Resident orchestration service** (`scripts/serve.py` + `entry.py` client): heavy modules are warmed up once, so local overhead → 0. Idle window raised 600s → 3600s (2026-10-16).
- **L2 Parallel warm-up** (`scripts/orchestrate.py`): eliminates stacked serial imports.
- **L3 Inline verification discipline**: sha256 is computed inline in memory and only on a suspected mismatch — the plain-text exit's trailing marker already proves completeness. Zero LLM round-trips.
- **L4 Single-command + unified session store (2026-10-16 · unified & multi-turn 2026-10-22 · **single path 2026-10-22**)**: `scripts/entry.py` now emits the **final plain-text answer in one call** — no decode step, no second script, and the payload shrinks from 4× (base64 of CJK) back to 1×. `scripts/ask.py` is retained only as a zero-logic forwarder for stale callers. The unified `scripts/session_store.py` (shared by **both** entry.py and the workbench proxy) gives a 30-min cross-session answer cache + a 10-min in-session near-duplicate dedup, so a re-send / repeated question costs **0 Coze calls**; it also injects multi-turn `conversation_history` into the Coze payload so context carries across rounds (previously the history was computed but never injected — root cause of 18% "承接上一轮" manual recaps). Root cause fixed: the `dedup_guard` short-circuit had never been reachable from `entry.py` (guard wired only into the `refine_answer.py` CLI; `query_origin` never set by entry.py), so every re-run was a real Coze round-trip — three of them for a single question in the 2026-10-16 log.
- **L5 Scope broadening via domain router (2026-10-22)**: `scripts/scope_guard.py` was rewritten as a controlled-vocabulary domain router (multi-label: compliance / ops / writing / design / stats / safety / registry / data / rws / methodology / medical / device / vet). The three real high-frequency blocks users actually use — **regulatory response / trial operations / deliverable drafting** — are now first-class in-scope core domains (a writing / outline / template question is NO LONGER treated as out-of-scope); only a clearly non-medical / non-life-science question (e.g. consumer electronics, finance, FMCG) emits a constructive referral. 0% out-of-scope on the 68 real questions from the past-30-day Feishu advisorlog.

**⚠️ Deployment restriction (important)**: the skill directory lives on a network share whose ACL is creator-owner — you can create new files, but **overwriting pre-installed existing files raises `PermissionError 13`**, and deletion is also blocked by a trash hook. Therefore, any change to `scripts/*.py` / `SKILL.md` should be written as a same-directory `.new` copy, then overwritten on the user's local machine with `move /Y` (command in `PERF_SOP.md` §4, or run `scripts/_perf_deploy.py`).

**Version drift**: the resident service caches code; after updating skill files, the old service still runs old code until its idle timeout (3600s since 2026-10-16; override with `CT_ADVISOR_IDLE`). `entry.py` has a built-in `/version` probe that, before reusing an old service, compares a **code fingerprint** — the max mtime across `scripts/*.py` + `adapters/**/*.py`, computed by `scripts/code_fingerprint.py` — against the value the service recorded at startup. If the local copy is newer it auto-shuts-down the old service and launches the new version. **No manual restart is ever required.** *(Before 2026-10-16 the probe compared only `orchestrate.py`'s mtime, so updating just `serve.py` or `adapters/**` silently failed to take effect — fixed in the same release.)*

A manual shutdown endpoint remains available for rescue scenarios — see `references/ADVANCED.md`. End users never need it.

## Session, Context, Cache & Routing

Local modules enrich the Coze payload: multi-turn `conversation_history`, 30-min cross-session answer cache, 10-min near-duplicate dedup, and a controlled-vocabulary domain router (`scope_guard`). All four capabilities are wired into both `entry.py` and the workbench proxy. Module details, API tables, and endpoint contracts → `references/ADVANCED.md`.

## Capability Domains — Expanded Coverage (2026-10-22)

Coverage was broadened per user mandate: the three previously-uncovered but high-frequency real-user blocks — **regulatory response / trial operations / deliverable drafting** — are now first-class in-scope core domains (mapped to `scope_guard` labels `compliance` / `ops` / `writing`). They are **never** empty-refused; only clearly non-medical / non-life-science questions get a constructive referral. Full sub-topic catalog + authoritative anchors (ICH / NMPA / CDE / TransCelerate / DIA / CASRAI / EQUATOR, searched 2026-10-22) live in **`docs/capability_domains.md`**. Summary:

| Domain (label) | What the advisor answers | Key authoritative anchors |
|---|---|---|
| Regulatory response `compliance` | GCP principles and applicability, China GCP implementation, inspection/audit readiness, protocol deviation and CAPA, safety reporting, registration and information disclosure (CTR number + 30-day deadline), regulatory correspondence / agency communication, informed consent and protection of vulnerable subjects | ICH E6(R3) 11 原则（2025-07-23 生效）· NMPA GCP 2020 第 57 号 · CDE《登记与信息公示管理规范》2020 第 9 号 + 平台 chinadrugtrials.org.cn |
| Trial operations `ops` | Site activation, TMF / essential documents (DIA TMF Reference Model v3 + MAGI ISF), monitoring models (RBM / centralised / hybrid), RBQM (QTL 1-5 / KRI 10-25, CtQ factors), vendor/CRO management, enrolment and retention, site close-out and DBL | TransCelerate RBM & QTL Framework · DIA TMF RM (tmfrefmodel.com) · ICH E8(R1) · CASRAI TMF 指南 |
| Deliverable drafting `writing` | Protocol (CPT/eCPT), SAP (ICH E9(R1) estimand five attributes + Gamble 55-item checklist), CSR, IB, ICF, device documentation (ISO 14155), registration documents | TransCelerate CC&R（2026 对齐 ICH M11）· ICH E9(R1) · EMA addendum · CASRAI SAP 模板 · EQUATOR |

Assistance boundaries (enforced in-engine, documented in the doc): ✅ explain clauses / give decision frameworks / checklists / templates; ⚠️ never substitute legal, regulatory, or medical-writing conclusions — route to `ct-registry` / `ct-stats` / `ct-samplesize` / submission path as noted. The three domains are **locally routed**; Coze only needs to honour `domain_hint`.

**Protocol-review routing (v1.3.39 · 2026-11-05):** when the question carries protocol-review intent (`方案` + `评阅/审阅/评审/审查/批注/修订/修改意见`, or `protocol review/audit/assessment`), `scripts/route_tool.py` appends an answer-footer **soft suggestion** pointing at the local `ct-protocol` skill (structured U1–U12 review / D1–D9 risk scoring / annotated output). It is **never auto-invoked** — `ct-protocol` is Tier B and absent from `tool_mapping`'s auto-execution table; the user decides whether to switch. Since 2026-11-09 the footer uses the directly-invocable `@skill:ct-protocol` mention. Details: `docs/capability_domains.md` §3.3.

**SAS→R migration routing (2026-11-11):** when the question carries SAS→R migration/porting intent (`迁 SAS 到 R` / `R 复刻 SAS` / `SAS 等价 R` / `SDTM/ADaM/TLF 的 R 版` / `SAS→R`), `scripts/route_tool.py` appends an answer-footer **soft suggestion** pointing at the local `ct-sas2r` hub skill (等价层 + 验证 SOP + 隐式业务规则恢复 + 分域编排). It is **never auto-invoked** — like `ct-protocol`, it is absent from `tool_mapping`'s auto-execution table; the user decides whether to switch. Since 2026-11-09 the footer uses the directly-invocable `@skill:ct-sas2r` mention. Details: `ct-sas2r/SKILL.md`.

## Client handoff contract (2026-11-09)

The client can now invoke sibling skills (`ct-safety` / `ct-registry` / `ct-literature`
and the rest of the locally registered `ct-*` family) directly. ct-advisor was adapted
to hand execution back to the skill itself instead of standing in for it:

- `handle_need_tool.execute_card` checks `_client_callable(tool)` **before** the tier
  gates. A locally registered skill returns `status=handoff`: a structured card with
  `@skill:<slug>`, params already extracted from the question, missing params, the
  skill's real deliverables and a Tier-B confidentiality note. No CLI subprocess, no
  SAFE PREVIEW bypass, no truncation-stitched summary. This also removes the stale
  "not publicly released / cannot be installed" wording for Tier-B and unlisted skills
  that are in fact installed locally.
- `refine_answer._merge_answer` renders that card into the answer body **in code**;
  `orchestrate.build_output` wraps it through the single `entry.py` exit. The local LLM
  still has exactly one allowed action (run `entry.py`, pipe stdout verbatim) —
  🔴 **HARD GATE unchanged**: the model must not choose a sibling skill, must not
  invoke one itself, and must not add or rewrite any text.
- `route_tool.suggest_footer` and `brief_contract.json::suggest_text` now share the
  same `@skill:<slug>` mention format; the footer covers Tier-B and unlisted skills too.
- Availability is **orthogonal** to `published` (SkillHub listing) and to `tier`
  (ct-base §11 `input_sensitivity`). Tier B is still a confidentiality boundary: being
  callable never licenses sending protocols / subject data to public endpoints (F33).
- Mixed-skill asks: every additional tool in `need_tools` gets its own
  `@skill:<slug>` card — params split by that skill's own CLI allowlist, missing
  params, deliverables and a Tier-B note — rendered in code by
  `refine_answer._render_deferred_cards`. The primary card is filtered the same way,
  so no cross-skill parameter leaks (e.g. `topic` never reaches `@skill:ct-registry`).
  Skills **not registered locally** are marked as such instead of getting a fake
  `@skill` card. `need_tools` is carried through the whole pure-code main flow
  (predict prefetch card, Coze `RefineResult.need_tools`, delegate block, card-inline
  and ship); `handle_need_tool.ensure_deferred()` backfills it if any upstream drops
  it, so a mixed question never degrades to a single card. Covered by
  `scripts/test_cross_skill_handoff.py` (28), `test_cross_skill_mixed_extended.py` (15)
  and `scripts/test_mainflow_mixed.py` (11 main-flow cases).
  **Return path**: `entry.py --stitch` (above) stitches sibling outputs locally once
  they exist — same single entry, zero egress, zero LLM. Chinese mixed questions now
  resolve `cond` / `topic` for ct-registry / ct-literature via
  `route_tool.extract_params_for_tools`; the single-skill `_extract_params` and its
  37/37 lexicon regression are untouched. ct-safety still leaves `drug` missing
  **on purpose** — openFDA only accepts English generic names — so its secondary
  card shows an explicit conversion hint instead of a harmful Chinese value.
- Rollback / opt-in: `CT_ADVISOR_HANDOFF=0` → legacy execution card (red line 2 keeps
  the local engine); `CT_ADVISOR_CLOUD_BRIEF=1` → non-audit brief shortcut, **default
  off** since the client can now reach the full skills. See
  `docs/cloud_brief_rollout_20261109.md` (evening re-evaluation, top of file).

## Consultation vs execution: intent layering & KB ownership (2026-11-09)

Sibling skills are **execution** capabilities (compute n, query registries, run
FAERS disproportionality, search literature). Questions about **why / what a
parameter means / how to interpret a result / on what authority** are
**consultation** and must be answered by ct-advisor itself from the Coze
knowledge base — not delegated to a data skill.

| Layer | Intent | Owner | Delivery |
|---|---|---|---|
| L1 | principle, parameter semantics, method choice, interpretation, regulatory rationale | ct-advisor + **Coze KB** | methodology answer with sources + optional trailing `@skill:` suggestion |
| L2 | compute / retrieve / export | sibling skill (client handoff) | `@skill:` card + params + deliverables |
| L3 | "what does this PRR / n mean" after results exist | Coze KB + **sanitized numeric summary** | `entry.py --stitch` with `"interpret": true` |

🔴 **Knowledge base ownership (user ruling 2026-11-09)**: all domain knowledge
lives **only on the Coze endpoint** (`adapters/coze/knowledge/`), maintained
there and shipped with the Coze package. **The local skill keeps ZERO knowledge
base** — no `knowledge/` directory, no `config/kb_topics.json`, no local
`methodology_anchors.md`. Three L1 topics (`ref-topic-samplesize-methods`,
`ref-topic-signal-methods`, `ref-topic-registry-semantics`), the L1 answer
contract, `_CATEGORY_KNOWLEDGE` routing and `knowledge_index.json` are all
Coze-side assets. The local side passes **only** `query_meta.domain_hint` for
category fallback; it must **never** put a domain into `scope_hint`, because the
cloud renders any non-empty `scope_hint` as "may be outside this skill's core
scope". See `docs/consult_intent_roadmap_20261109.md`.

Intent classification is pure code: `config/intent_contract.json` is the single
source of truth, with embedded copies in local `route_tool.py` and cloud
`tool_router_node.py`, locked by the `check_route_drift.py` AST gate. Cloud
changes require **republishing the Coze package** — the v1.60 build is
`adapters/coze/ct-advisor_coze_v1.60_20261109.zip`; until it is deployed the
live endpoint still runs the previous rules. Regression:
`scripts/test_consult_intent.py` (35 offline cases).

## Requirements

| Item | Requirement |
|---|---|
| Runtime | `python3` stdlib only |
| Sibling skills | **Client-callable since 2026-11-09**: the client can invoke every locally registered `ct-*` skill directly. Availability is decided by `scripts/sibling_registry.json` (`skills[*].installed`) plus `<SKILLS_DIR>/<slug>/SKILL.md`, implemented in `handle_need_tool._client_callable()` — **not** by SkillHub listing. `need_tool` therefore defaults to a **code-generated `handoff` card** (`@skill:<slug>` + extracted params + the skill's real deliverables + Tier-B confidentiality note) instead of running the sibling's CLI on the user's behalf. `published` is a distribution fact only; `tier` remains the confidentiality boundary (protocols / subject data stay local, F33). `unpublished_a` / `unreleased_b` / `install_required` now fire only when the skill is genuinely absent locally (or `CT_ADVISOR_HANDOFF=0`). |
| Refiner (Coze) | `scripts/entry.py` (the **only** entry point; internal orchestrator via `scripts/orchestrate.py`) sends payload to `ct-advisor.coze.site` — **async-first** (v1.3.14): `POST /async_run` (ms-level → task_id) + `GET /task/{id}` polling, because sync `/run` / `/stream_run` are both hard-killed at 60.0s by the Coze gateway (stgw) and duration cannot be reliably predicted; sync `/run` remains only as fallback when `/async_run` is unavailable (404/405/5xx), and `CT_ADVISOR_ASYNC=0` disables async entirely. Credential embedded in `adapters/coze_token_embedded.py` (obfuscated public token — keep as-is). 90s timeout / 300s long timeout (= polling deadline in async mode). |
| External Refs | **teal** (insightsengineering) — clinical-data interactive exploration framework; **Docling** — structured PDF parsing. See "External Tool References". |

## Attachment handling (docx / xlsx / pptx · doc / xls / ppt · pdf)

**Single gate = 5 MB, decided FIRST inside `entry.py` (v1.1.0 workflow correction, 2026-09-25). BOTH paths deliver a FILE to Coze through the same `doc_context` channel.**

| Size | Behavior | Channel |
|---|---|---|
| `< 5 MB` | **Upload the original file directly** — never converted locally | `doc_memory.build_file_payload(allow_upload=True)` → Coze `/upload_file` → `doc_context` (`mode=file_id`); on upload failure auto-degrades to the base64 forward channel (`mode=file`) |
| `> 5 MB` | Convert to Markdown locally, then **upload the resulting `.md` as the attachment** — same `doc_context` channel — plus an ℹ️ notice that the cloud answers from the md version | `scripts/office_to_md.py` (stdlib-only; OOXML) or direct read (`.txt/.md/.csv/.tsv/.json`); unsupported formats get an explicit user prompt |

Coze decodes the original file natively for **any** Office format (OLE2 `.doc/.xls/.ppt` included), so fidelity is higher than any local conversion — this is why the <5 MB path uploads instead of converting.

**Governance pointer**: layered conversion strategy, user prompts and confidentiality boundary are consolidated in **ct-base §6.7**; the shared converter lives in `ct-base/scripts/office_to_md.py` (vendored copy).

**Deliverable boundary — the revised document is never returned (v1.24).** This skill's deliverable is **text only**: it does not generate, export, or hand back a modified document file. When the user asks for the revised file back, state plainly on the **first line** that **this feature is not available — only written suggestions are provided**, then give the suggestions as text the user can copy.

## Quality Gate & Stop Rules

**Presentation rules (user-mandated, hard)** — deliver only the plain-text answer printed by `scripts/entry.py` (everything above the trailing `<<<CT_ANSWER_END>>>` marker). **Never emit any workflow / process narration to the user.**

**🔔 Forward-mode user notice (the ONLY allowed process message)** — entry.py emits a brief notice to stderr before firing the Coze call. The local LLM should not add any additional process chatter.

## Outbound Authorization Gate

Runs automatically inside `entry.py` → `scripts/orchestrate.py` before each outbound HTTP call (agent never triggers it manually). Endpoint `https://ct-advisor.coze.site/run` is in `auto_approve_endpoints` by default, so it never prompts. If the user wants another endpoint whitelisted across sessions, the USER adds it explicitly to `config.json` — **the agent MUST NOT edit `config.json`**.

## External Tool References (v1.3.4 · external authoritative assets)

- **teal** (insightsengineering, `install.packages('teal')`) — clinical-data interactive exploration framework for building Shiny review apps; reference model for the data-review integration mode.
- **Docling** (`pip install docling`) — structured parsing of regulatory documents (protocol/IB/CSR PDFs → hierarchical Markdown/JSON); attachment-parsing enhancement layer.
- **Pinnacle 21 Validation Rules** (Certara, public API `standards.pinnacle21.certara.net/validation-rules/<STD>`, header `X-Requested-With: XMLHttpRequest`) — industry-standard CDISC validation rule set; snapshots archived in `ct-base/references/pinnacle21_validation_rules/` (SDTM 566 / SEND 581 / ADaM 456 / Define-XML 167). Authoritative benchmark for data-standard compliance Q&A; mirrored to Coze KB topic `ref-topic-p21-data-rules`.
- **ICH M12 DDI Thresholds** (Step 4/5 official PDFs archived alongside `ct-base/references/m12_thresholds.md`) — CYP 50× / intestinal 10×, TDI 1.25, induction R-ratio, transporter Table 1, AUCR 0.80–1.25, GMR 90% CI 80–125%. Authoritative benchmark for DDI interaction Q&A; mirrored to Coze KB topic `ref-topic-m12-ddi`.

## Bug Report (§20.3 · ct-base)

On defect detection or explicit user request, `adapters/bug_report.py` offers a sanitized 11-key report to `https://ct-bugreport.coze.site/run`. Two-stage confirmation mandatory.


## Error Self-Heal Protocol (stderr machine signals · 2026-10-15)

**Scope — failure paths ONLY.** On a successful run (`scripts/entry.py` exits 0 and prints the answer, and **no `[ct-advisor][ERR]` line on stderr**), the agent delivers the answer and stops. **The agent MUST NOT enter self-healing when no error was reported** — no proactive health checks, no proactive dependency installs, no proactive config/env edits, no speculative retries. The `[ct-advisor][ERR]` signal is the **only** trigger.

> **Where signals live (2026-10-16)**: the resident service (`scripts/serve.py`) is spawned with `stderr=DEVNULL`, so anything written inside the service process — including an `[ct-advisor][ERR]` emitted on the service path — is redirected by the service itself to **`config/serve.log`** (auto-truncated at 1 MB). If `entry.py` prints no `<<<CT_ANSWER_END>>>` marker (empty or destroyed stdout) while stderr carries no `[ERR]` line, read the tail of `config/serve.log` before concluding anything.

**Signal format (single line, stderr):**

```
[ct-advisor][ERR] code=<CODE> auto_fixable=<true|false> retry_safe=<true|false> requires_network=<true|false> [detail="…"] [fix_cmd="…"]
```

**Code → agent action:**

| code | auto_fixable | retry_safe | requires_network | Agent action |
|---|---|---|---|---|
| `CONN_FAIL_PROXY` | false | true | true | Deliver the answer-block text verbatim (it carries numbered recovery steps). Offer **one** retry only after the user confirms the proxy/network is fixed. Never edit env or config yourself. |
| `CONN_FAIL_DIRECT` | false | true | true | Same as above. |
| `TIMEOUT` | false | **false** | true | Deliver verbatim. **Never auto-retry** — Coze likely already received the request; a blind retry duplicates it. |
| `AUTH_401` | false | false | false | Deliver verbatim; explain the token must be renewed by the skill maintainer. Do not edit any skill file. |
| `COZE_HTTP_ERROR` | false | false | true | Deliver verbatim; a user-initiated retry after 1–2 minutes is acceptable. |
| `ORCH_FAIL` | false | false | false | Deliver verbatim; ask the user to report the `detail` field to the skill maintainer. |

**Hard rules (violating any of these is a defect):**

1. **No signal → no action.** Absence of `[ct-advisor][ERR]` means success; the agent must not probe, install, edit, or retry anything.
2. `fix_cmd` may be executed **only** when `auto_fixable=true` (after the 2026-10-15 stdlib-urllib transport change, **no code currently qualifies** — the dependency-missing class was eliminated) **and** the user has explicitly confirmed. Execute it **verbatim**; never improvise commands; never edit skill files or `config.json` (same red line as the Outbound Authorization Gate).
3. At most **one** retry per user turn, only after a successful fix, and only when `retry_safe=true`.
4. `requires_network=true` means the fix itself needs working outbound access — resolve network-class errors first.
5. Self-healing covers **transport repair only**. It never licenses local answer generation — the coze-only red line stands.
6. If stderr carries an `[ERR]` line but stdout has no answer block, treat the turn as failed: relay the signal's meaning plus any human-readable guidance. **Never fabricate an answer.**
7. Signals are emitted from failure paths only (`adapters/errsignal.py::emit_err_signal`). If an `[ERR]` line appears on a run that returned a valid answer, treat it as a skill defect and report it.

**Note on `[DEP-MISS]`:** before 2026-10-15 a missing `requests` library surfaced as `[DEP-MISS]` + an install prompt. The transport now uses stdlib `urllib`, so this failure class no longer exists; the handler remains as dormant defensive code.

**2026-10-26 · ct-base §22.24 dual-track governance framework**: as the ct-series single entry point routing to ct-samplesize/ct-registry/ct-safety/ct-literature/ct-protocol, any classification judgement involving AI-as-intervention (prospective evaluation + SPIRIT-AI/CONSORT-AI) vs AI-for-trial-operations (workflow accuracy + TRIPOD-AI/ICH E6(R3)) follows the §22.24 dual-track governance framework (EClinicalMedicine 2026-10).

---

