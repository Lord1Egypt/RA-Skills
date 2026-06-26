# OpenClaw + DanceTempo

This reference aligns **OpenClaw** workspace usage with the **DanceTempo** repo and documents the **optional bootstrap hook** (parity with [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent)).

## Optional: bootstrap hook

Injects a **virtual** file **`DANCETEMPO_CONTEXT_REMINDER.md`** on **`agent:bootstrap`** so every session sees pointers to **`public/llm-full.txt`**, **`CLAWHUB.md`**, and **`GET /api/dance-extras/live`**. Sub-agent sessions are skipped.

**Install** (from this skill directory):

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/dancetempo-clawhub
openclaw hooks enable dancetempo-clawhub
```

**Disable:**

```bash
openclaw hooks disable dancetempo-clawhub
```

**Files:** `hooks/openclaw/HOOK.md`, `handler.js`, `handler.ts`.

No secrets, no network calls.

---

## Workspace files (manual injection)

If you use `~/.openclaw/workspace/`:

| Workspace file | DanceTempo equivalent |
| --- | --- |
| **`AGENTS.md`** (workspace) | Repo **`AGENTS.md`** if present; else **`README.md`** “Routes” + **`DANCETECH_USE_CASES.md`** |
| **`TOOLS.md`** | Integration notes in **`CLAWHUB.md`** + **`server/index.js`** headers |
| **`MEMORY.md`** | Not used in-repo; use **`CLAWHUB.md`** for durable tribal notes |

## Minimum injection blurb

Add to workspace **`AGENTS.md`** or session bootstrap if you **do not** use the hook:

```markdown
## DanceTempo
- Full context: `public/llm-full.txt` (regenerate: `npm run build:llm`)
- Debugging: `CLAWHUB.md`
- API smoke: `GET http://localhost:8787/api/dance-extras/live`
```

## Skills directory

Copy this skill for offline use:

```bash
cp -r /path/to/dancetempo/.cursor/skills/clawhub ~/.openclaw/skills/dancetempo-clawhub
```

Skill entry remains **`SKILL.md`** inside that folder.
