# Channel Formatting

Format the audit output for the current channel. The agent knows which channel it's delivering to.

## Slack

Blockquotes for findings, bold headings, `_· · ·_` separators, `─────────` under title.

**Audit output (before fix):**

```
🔍 *Portability Audit — `acme-email-skill`*
─────────────────────────────────────

*6/8 checks passed · ❌ 2 issues · 🔧 2 auto-fixable · ⚠ 1 manual*

❌ *Issues (auto-fixable with --fix)*

> `~/.openclaw/credentials/token.json`
> → scripts/check_gmail.py:28

> `~/.openclaw/workspace/data/history/`
> → scripts/check_gmail.py:35

_· · · · · · · · · · · · · · · · · · · · · · · · · · ·_

⚠ *Manual review needed*

> clawhub CLI in scripts/publish.py:42
> Platform-specific dependency — cannot auto-fix

─────────────────────────────────────
📌 *2 auto-fixable · 1 manual · Run with `--fix` to apply*
```

**Fix confirmation (after --fix):**

```
✅ *Fixed: 2 issues resolved*

> `~/.openclaw/credentials/token.json` → `$SKILL_DATA_DIR`
> in scripts/check_gmail.py

> `~/.openclaw/workspace/data/history/` → `$SKILL_DATA_DIR/history/`
> in scripts/check_gmail.py

⚠ *1 manual item still needs review*
```

**Clean audit (fully portable):**

```
✅ `acme-email-skill` — Fully portable
   All 8 checks passed
```

## WhatsApp

No blockquotes, no code formatting, no markdown tables. Bold repo names only. `─────` separators.

**Audit output:**

```
🔍 Portability Audit — acme-email-skill
─────────────────────────────────────

6/8 checks passed · ❌ 2 issues · 🔧 2 auto-fixable · ⚠ 1 manual

❌ Issues (auto-fixable with --fix)

~/.openclaw/credentials/token.json
→ scripts/check_gmail.py:28

~/.openclaw/workspace/data/history/
→ scripts/check_gmail.py:35

─────────────────────────────────────

⚠ Manual review needed

clawhub CLI in scripts/publish.py:42
Platform-specific dependency — cannot auto-fix

─────────────────────────────────────
📌 2 auto-fixable · 1 manual · Run with --fix to apply
```

## Discord

Similar to Slack but no blockquotes (Discord ignores `>` on multi-line). Use `**bold**` headings, `` `code` `` for file paths, `─────` separators.

## Terminal

Use raw script output as-is. No formatting changes needed.
