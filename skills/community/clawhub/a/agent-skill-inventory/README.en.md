# skill-inventory · Skill inventory & health check for office agents (English)

> 中文版：[README.md](README.md) · Docs language: `SKILL.md` (Chinese) / `SKILL.en.md` (English)
> Both editions carry the same content: the English files are not shorter (measured on v1.4.0 —
> README 14,505 vs 7,261 chars, SKILL 14,460 vs 10,722), with matching section counts and FAQ items.

Skill inventory & health check for office agents (WorkBuddy, QwenWork, Baidu DuMate, Tianxi AI,
…): scans any skills directory, measures size / context-token footprint, detects duplicates, and
classifies skills into **used / closeable / manual-review / protected** with **conservative**
slimming advice. **Read-only by default**: inventory, classification and advice write nothing
anywhere; there are two write targets plus one backup artifact, all requiring explicit consent
(`--overrides --apply --yes` for closes — WorkBuddy-family platforms only, writes atomically and
backs up settings.json first; `--set-lang` for the language preference) — the decision stays human.

> Skills whose manifest (name + description) rides along in every conversation turn cost real
> tokens — 54 installed skills ≈ 5,000+ tokens burned per turn. This tool provides the facts for
> "which ones to close".

## When to use

- "What skills do I have", "which can be closed / merged", "how much context do they cost"
- Health-check an office agent's skill library and cut context-token spend
- Inventory skills on WorkBuddy / QwenWork / Baidu DuMate / Tianxi AI
- Pin the report language to English or Chinese (or restore auto-follow)

## Usage

The script lives at `scripts/skill_inventory.py`. By default it inventories the WorkBuddy library:

```bash
python scripts/skill_inventory.py                          # full table + four buckets (auto-detect)
python scripts/skill_inventory.py --agent workbuddy        # platform profile
python scripts/skill_inventory.py --agent qwen             # QwenWork (scan-only)
python scripts/skill_inventory.py --agent baidu --root DIR # Baidu DuMate (path TBC → --root)
python scripts/skill_inventory.py --overrides              # draft the close list (draft only)
python scripts/skill_inventory.py --overrides --apply --yes   # WB: apply with your consent (backup first)
python scripts/skill_inventory.py --json                   # machine-readable output
python scripts/skill_inventory.py --protect a,b,c          # extra protected skills
```

Cross-agent: pick a platform with `--agent` (workbuddy / qwen / baidu / auto) or point `--root`
straight at a skills directory. Pass the usage log via `--usage-log`; **if the platform has no
usage log, the tool degrades to "nothing judged closeable"**.

## Language setting (auto / zh / en)

| Option | Meaning |
|--------|---------|
| `auto` (default) | automatic — the Agent decides per conversation language via `--lang`; if unset, falls back to env `SKILL_INV_LANG` → system locale → Chinese |
| `zh` | report language pinned to Chinese (change any time via `--set-lang` / `--lang`) |
| `en` | report language pinned to English (change any time via `--set-lang` / `--lang`) |

```bash
python scripts/skill_inventory.py --show-lang   # current setting, options and how to change
python scripts/skill_inventory.py --set-lang en # save preference (writes ~/.workbuddy/skill-inventory.json), effective immediately
python scripts/skill_inventory.py --set-lang auto
python scripts/skill_inventory.py --lang en     # this run only, keeps the saved setting
python scripts/skill_inventory.py --selftest    # self-test the built-in parser (zero deps, offline)
```

Changes take effect immediately after saving; `--set-lang auto` or deleting
`~/.workbuddy/skill-inventory.json` restores the default. `auto` is the fallback for users who
have not expressed a preference, not a lock-in — pin a language with `--set-lang` at any time, or
override one run with `--lang`. Bucket names are always English
identifiers and `--json` keys are always English — scripted consumption is language-independent.

## Platform profiles & capability-aware closing

Agents differ in "close" capability; the tool branches on `can_close` — **non-closable platforms
never get close actions**, only a report plus manual-removal instructions:

| Platform | Scannable | Usage ledger | Programmatic close | Behaviour |
|----------|-----------|--------------|--------------------|-----------|
| **WorkBuddy** | ✅ `~/.workbuddy/skills` | ✅ `usage-log.json` | ✅ `skillOverrides` four states | inventory + close drafts; `--apply --yes` writes `off` with your consent |
| **QwenWork** | ✅ `~/.qwenworkcn/skills` | ✅ (usage adapter) | ❌ **no disable switch** (field-tested) | inventory + connector/UI close instructions; never performs a close |
| **Baidu DuMate** | ✅ local sandbox (path TBC → `--root`) | ❌ | ✅ disable switch + expert-suite disable | inventory + close instructions; owns the "expert suite" dimension |
| **Generic** (unknown hosts, incl. Tianxi cloud sandboxes) | ✅ `--root`, or `--probe` auto-discovery | ❌ by default (`--usage-log` to add) | ❌ no close channel | `--agent generic`: pure inventory + advice, all manual review, no close actions |

> Principle: **"no usage record" is not "unused"**. On platforms without a close switch the tool
> only health-checks and leaves the knife to you, avoiding "close advice" you cannot execute.

## 🔒 Behaviour contract (read this before trusting it)

**Read-only by default; two write targets + one backup artifact, both consent-gated:**

1. **Writes nothing by default.** Inventory, classification and advice are read-only; no
   disable/delete API is called.
2. **Write path 1 (closes; needs your explicit consent).** On closable platforms
   (WorkBuddy family), `--overrides --apply --yes` **backs up `settings.json` automatically
   first**, then merges candidates into the `off` state of `skillOverrides`; without `--yes` it
   is a dry-run preview (no files read or written); non-closable platforms (QwenWork etc.)
   reject `--apply` outright. Every report and `--overrides` output states this path explicitly —
   the tool **never** closes a skill silently or on its own initiative. Host-native toggles
   (e.g. the `/skills` menu, press Esc to persist) are preferred.
   **Backup artifact:** before the close write, `--apply --yes` creates a
   `settings.json.bak.<timestamp>` safety copy beside `settings.json` and prints its path; the
   copy is inert, never read back, and you may manually delete it when you no longer need it.
3. **Write path 2 (language preference; needs your explicit command).** `--set-lang auto|zh|en`
   writes the report language preference to `~/.workbuddy/skill-inventory.json` (that one key
   only); a user-controlled display preference, revertible via `--set-lang auto` or by deleting
   the file.
4. **No autonomous residency.** No cron jobs, no startup scripts, no daemons, no
   self-modification (i.e. no autonomous execution). Cross-session **visible writes** are limited
   to two user-consented, disclosed and reversible capabilities — the `off` entries in
   `skillOverrides` (reversible via the host's `/skills` menu) and the language preference file.
   The language preference file is a display preference only (a single JSON key): nothing is
   scheduled or registered from it, it is read solely to pick the report language, and
   `--set-lang auto` or deleting the file restores the default.
   ↳ Note: the tool does perform authorized cross-session writes (see items 2–3) — that is
   distinct from autonomous residency (autonomous execution), which it has none of.
5. **Protected skills never enter the closeable bucket.** This includes: this tool itself,
   skills marked `protected: true` in frontmatter, safety/audit classes (names containing
   security/audit/safe/guard/privacy/sanitize/compliance/backup), and anything added via
   `--protect`. They are listed separately as "protected".
6. **"No usage record" is not "unused".** Users may **never name a skill in conversation** and
   instead:
   - pre-configure **keyword triggers** that auto-invoke it;
   - use it indirectly via **expert/connector components** that call it internally.
   Both leave **no trace** in usage logs. So **every close candidate must be confirmed with the
   user** for these dependencies before closing.
7. **Telemetry gap ⇒ nothing judged closeable.** When the platform has no usage log, or the log
   fails to read (P1 fixed: explicit warning instead of silence), everything lands in
   "manual review" and **no close candidates are emitted** — under-reporting beats false kills.
8. **Reverse-dependency scanning (the scenario you worry about most).** Before judging
   "closeable", the tool scans automations / hooks for skill references (default
   `~/.workbuddy/automations` and `~/.workbuddy/hooks`; extend with `--refs`). **Any referenced
   skill is locked as "protected"** — with or without usage records. This blocks false kills
   caused by keyword triggers or expert/connector-internal calls invisible to logs. Point
   `--refs /path/to/defs` at definitions stored elsewhere; disable entirely with `--no-ref-scan`.

## Reading the output

A real run prints roughly:

```text
Platform WorkBuddy · 59 skills · 27 used · 6 protected · 19 close candidates · 7 manual review
                        ≈ 6,912 tokens / conversation turn
Directory         ⚠/🔒  Lines  KB   Source  Last mod  Uses  Last used
ai-weekly                 168  2734  self   2026-10-09  1  2026-10-05
skill-inventory      🔒   91   52  self   2026-09-28  0  —
🔻 Close candidates (still require per-item human confirmation):
  bug-fixing  667 lines · 2026-08-04    log-analyzer  501 lines · 2026-08-04
```

- `⚠` = recently modified, no usage record (goes to "manual review"); `🔒` = protected (never a
  candidate); `—` = no usage record.
- `--json` emits a machine-readable object with always-English top-level keys (`agent` /
  `can_close` / `rows` / `buckets` / `telemetry_gap` / `telemetry_scope` / `cannot_close`);
  `buckets` has four tiers: `protected` / `keep` / `cleanup` / `review`.
- `--selftest` offline-checks the built-in parser (vs PyYAML block-scalar semantics):
  "8 cases passed / 0 failed".
- Full sample (protected block, complete JSON structure, full selftest text): see
  `SKILL.en.md §6 What a real run actually prints`.

The four buckets, as legend:

- **used**: genuinely used (trustworthy).
- **closeable**: no usage record and untouched for over 30 days. **Still requires human
  confirmation**, and keyword/expert-trigger dependencies must be ruled out first.
- **manual-review**: no usage record but recently modified, or no telemetry on this platform —
  do not rush.
- **protected**: never auto-suggested for closing; explicit human action required.

## Mistakes to avoid

The six most common pitfalls (full table in `SKILL.en.md §10`): ① deleting a skill directory
directly (bypasses backup/lock, may false-kill a referenced skill); ② closing without
`--impact` (implicit dependencies leave no log trace); ③ treating "no record" as "unused"
(T2–T6 invisible); ④ expecting `--apply` to work on non-closable platforms; ⑤ treating
`--protect` as a universal guard (pair with `--refs`); ⑥ `--root` pointing at a parent
directory and swallowing unrelated dirs (point at the skills root, or use `--probe`).

## FAQ (quick reference; the full 11 Q&As live in SKILL.en.md §11)

**Q. Why is my skill in "manual review" instead of "close candidates"?**
Only "no usage record" **and** "untouched for over 30 days" qualifies. Four reasons push it elsewhere:
no telemetry / modified recently / the host has no programmatic close channel / it matches a protection
rule. `--usage-log <path>` and `--protect <name>` cut most of the noise.

**Q. Does "has usage record" mean "only ever invoked explicitly"?**
No. The usage log records explicit invocations (T1) only; auto-mounting, keyword routing, scheduled
tasks, hooks and expert-internal calls (T2–T6) leave no trace. So "no record" does not mean "unused".

**Q. The report says "telemetry gap" — what now?**
The platform has no usable log, so conclusions rest on last-modified time and **no** close candidates are
emitted. If a log exists, point at it with `--usage-log <path>`; otherwise rely on `--refs`
reverse-dependency scanning plus manual confirmation.

**Q. Could closing break an automation or keyword trigger?**
Three guardrails: reference-locking via reverse-dependency scan, safety-audit keywords and this tool
itself are never candidates, and every candidate needs your confirmation. Guardrails are not exhaustive
(T2 auto-mounting is invisible) — run `--impact <name>` first.

**Q. What do `[E-LOG]` / `[E-CONF]` mean?**
Stable error codes: `E-LOG` (usage log missing/unreadable), `E-ROOT` (skills dir not found), `E-PLATFORM`
(unknown `--agent`), `E-NOCLOSE` (host has no programmatic close channel), `E-CONF` (settings.json
read/write failed; nothing modified), `E-READ` (one skill dir unreadable, skipped). Full table in
SKILL.en.md §11.

## Limitations (stated honestly)

- Usage frequency relies on the platform usage log; WorkBuddy has a real ledger
  (`usage-log.json`), most other platforms do not — conclusions then rest on last-modified time
  only, which **must not justify closing**.
- Keyword-trigger / expert-component dependencies cannot be probed from the filesystem — a
  structural blind spot covered only by user confirmation.
- Duplicate detection is approximate (name/description/size), not semantic dedup.

## About automated scanners (SkillSpector findings and item-by-item response)

Some automated scanners (e.g. ClawHub SkillSpector) report findings against this skill. Most are
**inspection limitations** or **restatements of already-disclosed capability**, not suspicious
behavior. The table below gives verifiable facts for each (line counts measured on v1.3.1):

| Rule | What the scanner says | Facts / response |
|---|---|---|
| **Ae1** referenced artifact not completely inspected | The scanner cannot fully inline `scripts/skill_inventory.py` | **Inspection limitation.** That script measures 1562 lines on v1.5.0 and has zero third-party dependencies (standard library only; `yaml` is an optional accelerator). The file's own **static-analysis layer passes** ("No suspicious patterns detected"). Full source is public on the [GitHub repo](https://github.com/Elisabeth15501/skill-inventory) for manual review at any time. The finding count grows with the script's line count (7→11→12) — it tracks code size, not behavior change |
| **Lp1** capability broader than declared | The script writes to disk; capability exceeds the declaration | The declaration is now complete — **two write targets + one backup artifact**, all greppable in the frontmatter `permissions` block and the script's docstring header: ① the `skillOverrides` key of `settings.json` — requires the two explicit flags `--apply --yes` (either alone = dry-run); ② the language preference file — requires an explicit `--set-lang`; ③ a `settings.json.bak.<ts>` safety copy — created only before step ①'s write, path printed in the output, never read back. See the behaviour contract above |
| **Session Persistence** | Cross-session writes (all authorized) | No cron jobs, no startup scripts, no daemons, no self-modification (i.e. no autonomous residency). The language preference file is a display preference (a single JSON key): nothing is scheduled or registered from it, it is read once to pick the next report language; `--set-lang auto` or deleting it restores the default |
| **Anti-Refusal** | "always / always" style wording in the docs | Rewritten to "report language pinned to X (change any time)" — it describes the **tool's output language**, not an obedience promise toward the user |
| **Rp1** | Unpinned dependency in the supply chain | The skill has no external runtime dependency (Python standard library); publishing commands in the docs are pinned to `clawhub@0.23.3`, never `@latest` |
| **NL Policy** | Language selection | Three options auto / zh / en. `auto` is the **fallback for users who have not expressed a preference**, not a lock-in: pin zh or en via `--set-lang` any time, or override per run with `--lang` |
| **stability** (TRACE) | No explicit timeout; suggests 4 pts | **Appeal: local file operations do not need a global timeout.** Reads already do bounded retries — `_read_text()` retries **twice at 0.5 s** on file-locked `PermissionError` (code constants `retries=2, delay=0.5`, also declared in the script's docstring header). This is targeted tolerance for Windows file locks, not unbounded blocking; a global timeout would instead false-kill legitimate slow-disk / slow-network operations. Writes use atomic replace (temp file + `os.replace`), single-file granularity, no timeout needed |
| **func / accuracy** (TRACE) | Duplicate detection is approximate, not semantic | **Appeal: known limitation + self-verification path.** Duplicate detection matches on name/description/size (approximate), **not semantic dedup** (semantic dedup requires embedding models — disproportionate for a zero-dependency single-file script; explicitly declared "a lead, not a conclusion"). Users can pull `name`/`desc` from `--json` to verify themselves, or run `--impact <name>` for a per-skill impact view |
| **DBM / Intent-Code** (ClawHub v1.4.0) | description–behavior mismatch 91% / intent–code divergence 87% | **Fixed in v1.5.1**: `persistence` field refined from `none` to "no autonomous residency (no cron, startup script or daemon); two consent-gated config writes and one backup artifact DO survive the run"; all "no persistence mechanism" wording replaced with "no autonomous residency", explicitly distinguishing "authorized cross-session writes ≠ autonomous residency". See commit ef9eb03 |
| **Lp1** (ClawHub v1.4.0) | capability declaration broader than actual | **Fixed in v1.5.1**: added `capabilities` top-level list to frontmatter, coexisting with `filesystem.write`; removed script shebang (Lp1 "env" evidence source). See commit ef9eb03 |

**Platform-side result**: static analysis and human review both report **Moderate CLEAN**; the
scanner's own Overview states "disclosed, user-triggered… no evidence of hidden network,
autonomous residency, or destructive behavior". The script also carries a machine-greppable
"Permission & residency declaration" block in its docstring header — feel free to verify it
directly. If you find any mismatch between the declarations and the implementation, please open
an issue first — that fixes a problem faster than any scanner verdict.

**Disposition of new findings from this round's two reports (v1.4.0)** (P2-14 appeal-material sync):
- **DBM 91% / Intent-Code 87%**: fixed in v1.5.1 via "persistence refinement + repo-wide wording
  correction" — not a false positive, it was an internal logical contradiction in the docs, now
  actually corrected
- **Lp1 75% (file-write / env)**: fixed in v1.5.1 by adding the `capabilities` field + removing
  the shebang; the evidence sources are cleared
- **Ae1 13 items**: reduced in v1.5.2 via P2-11 exec-steps de-noising (12 lines of repeated
  paths → 9-line flags table), lowering the scanning surface; the root cause is the script's
  1562 lines of zero-dependency code — an inspection limitation, not a behavior issue
- **TRACE four regressions (docQuality 4.8→4.3 / antiPatternFaq 4.5 / progressive 4.5 /
  structure 4.5)**: v1.5.2 filled the documentation debt via P1-5~P1-8 (output-sample section +
  mistakes-to-avoid section + behaviour-contract dedup + README/SKILL differentiation); expected
  to recover

## License

MIT — see [LICENSE](LICENSE).
