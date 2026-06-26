# OpenClaw + Clinical Tempo

This reference aligns **OpenClaw** workspace usage with the **Clinical Tempo** repo and documents the **optional bootstrap hook** (parity with [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent)).

## Optional: bootstrap hook

Injects a **virtual** file **`CLINICAL_TEMPO_CONTEXT_REMINDER.md`** on **`agent:bootstrap`** so every session sees pointers to **`public/llm-full.txt`**, **`CLAWHUB.md`**, and **`GET /api/dance-extras/live`**. Sub-agent sessions are skipped.

**Install** (from this skill directory):

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/clinicaltempo-clawhub
openclaw hooks enable clinicaltempo-clawhub
```

**Disable:**

```bash
openclaw hooks disable clinicaltempo-clawhub
```

**Files:** `hooks/openclaw/HOOK.md`, `handler.js`, `handler.ts`.

No secrets, no network calls.

---

## Optional: **Anyway** OpenClaw plugin (`@anyway-sh/anyway-openclaw`)

The Clinical Tempo skill does **not** bundle third-party plugins. For OpenClaw users who want **Anyway** capabilities alongside this repo’s skill:

```bash
openclaw plugins install @anyway-sh/anyway-openclaw
openclaw plugins list
# If your gateway needs a reload:
openclaw gateway restart
```

- **Clinical Tempo skill** → *what to read* (`llm-full.txt`, `CLAWHUB.md`, API smoke tests).
- **Anyway plugin** → *extra tools/integrations* inside OpenClaw (upstream package; trust path per your org).

Install order does not matter; both can coexist.

---

## Workspace files (manual injection)

If you use `~/.openclaw/workspace/`:

| Workspace file | Clinical Tempo equivalent |
| --- | --- |
| **`AGENTS.md`** (workspace) | Repo **`AGENTS.md`** if present; else **`README.md`** “Routes” + **`HEALTHTECH_USE_CASES.md`** |
| **`TOOLS.md`** | Integration notes in **`CLAWHUB.md`** + **`server/index.js`** headers |
| **`MEMORY.md`** | Not used in-repo; use **`CLAWHUB.md`** for durable tribal notes |

## Minimum injection blurb

Add to workspace **`AGENTS.md`** or session bootstrap if you **do not** use the hook:

```markdown
## Clinical Tempo
- Full context: `public/llm-full.txt` (regenerate: `npm run build:llm`)
- Debugging: `CLAWHUB.md`
- API smoke: `GET http://localhost:8787/api/dance-extras/live`
```

## Skills directory

Copy this skill for offline use:

```bash
cp -r /path/to/clinicaltempo/.cursor/skills/clawhub ~/.openclaw/skills/clinicaltempo-clawhub
```

Skill entry remains **`SKILL.md`** inside that folder.
