# OpenClaw integration — Clinical Tempo (ClawHub skill)

Complete setup guide for using **this skill** with [OpenClaw](https://openclaw.ai/) and publishing on [ClawHub](https://clawhub.ai/). Structural parity with [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent): workspace injection, hooks, optional scripts.

## Overview

| Layer | Role |
| --- | --- |
| **`public/llm-full.txt`** | One-shot repo orientation (regenerate: `npm run build:llm`)
| **`CLAWHUB.md`** | Tribal debugging — successes, failures, checklists
| **This skill** (`SKILL.md`) | Tells agents *where* to find the above and *common traps*
| **Optional hook** `clinicaltempo-clawhub` | Injects bootstrap reminder (`hooks/openclaw/`)

## Install the skill

### From ClawHub (recommended)

Browse **[clawhub.ai](https://clawhub.ai/)**, find **Clinical Tempo** / **`arunnadarasa/clinicaltempo`**, and install with the site’s CLI (or download the zip).

Example (when the CLI supports your listing slug):

```bash
npx clawhub@latest install arunnadarasa/clinicaltempo
```

If the CLI syntax differs, use the **Publish** page instructions on the site.

### From this repository (authoritative)

```bash
git clone https://github.com/arunnadarasa/clinicaltempo.git
cp -r clinicaltempo/.cursor/skills/clawhub ~/.openclaw/skills/clinicaltempo-clawhub
```

Skill entry file: **`SKILL.md`** inside that folder.

### Optional: `_meta.json` for tooling

After publishing on ClawHub, you may copy **`_meta.sample.json`** → **`_meta.json`** and fill **`ownerId`** / **`publishedAt`** from the site UI (or keep only the sample in git for reproducible zips).

---

## Workspace structure (OpenClaw)

```
~/.openclaw/
├── workspace/                 # Injected prompts (optional manual copies)
│   ├── AGENTS.md
│   ├── SOUL.md
│   ├── TOOLS.md
│   └── MEMORY.md
├── skills/
│   └── clinicaltempo-clawhub/   # or: clawhub from repo path
│       └── SKILL.md
└── hooks/
    └── clinicaltempo-clawhub/   # optional — copy from skill/hooks/openclaw
        ├── HOOK.md
        └── handler.js
```

---

## Injected prompt alignment

| OpenClaw workspace file | Clinical Tempo source |
| --- | --- |
| **AGENTS.md** | Repo **`README.md`** routes + **`HEALTHTECH_USE_CASES.md`**
| **TOOLS.md** | **`CLAWHUB.md`** integrations + **`server/index.js`**
| **MEMORY.md** (long-term) | Prefer **`CLAWHUB.md`** for durable *incident* notes (committed) |

Minimum blurb for workspace **`AGENTS.md`**:

```markdown
## Clinical Tempo (HealthTech Protocol)
- Full context: clone repo `public/llm-full.txt` or run app `/llm-full.txt`
- Debug: `CLAWHUB.md`
- API smoke: `GET http://localhost:8787/api/dance-extras/live`
```

---

## Install the hook (optional)

Injects **`CLINICAL_TEMPO_CONTEXT_REMINDER.md`** on **`agent:bootstrap`**. No network I/O.

```bash
cp -r /path/to/clinicaltempo/.cursor/skills/clawhub/hooks/openclaw ~/.openclaw/hooks/clinicaltempo-clawhub
openclaw hooks enable clinicaltempo-clawhub
```

Disable: `openclaw hooks disable clinicaltempo-clawhub`

Details: **`hooks/openclaw/HOOK.md`**, **`references/openclaw-clinical-tempo.md`**.

---

## Optional: Anyway plugin

Separate npm package — extra OpenClaw runtime capabilities:

```bash
openclaw plugins install @anyway-sh/anyway-openclaw
```

See **`references/openclaw-clinical-tempo.md`**.

---

## Inter-session patterns

When OpenClaw exposes **sessions_** tools, use them to hand off **file paths** (`CLAWHUB.md`, `server/index.js`) and **network** (testnet vs mainnet) so sub-agents do not re-discover the same traps.

---

## Promotion workflow (repo memory)

| Finding | Where |
| --- | --- |
| Stable product fact (routes, ports, env *names*) | **`README.md`**, **`HEALTHTECH_USE_CASES.md`**, **`docs/*.md`** → then **`npm run build:llm`**
| Incident / debugging narrative | **`CLAWHUB.md`** Successes / Failures |
| Copilot default context | **`.github/copilot-instructions.md`**

Never commit secrets — use **`.env.example`** names only.

---

## See also

- **`SKILL.md`** (main skill)
- **`references/hooks-setup.md`** — Claude Code / Codex UserPromptSubmit hooks for `activator.sh`
- **[ClawHub](https://clawhub.ai/)** — publish and browse skills
