# `clawhub` — Clinical Tempo · [ClawHub](https://clawhub.ai/) skill

Authoritative copy: **`.cursor/skills/clawhub/`** in the **[Clinical Tempo](https://github.com/arunnadarasa/clinicaltempo)** monorepo.

**Published listing:** [clawhub.ai/arunnadarasa/clinicaltempo](https://clawhub.ai/arunnadarasa/clinicaltempo)

**Rigor model:** Same **package shape** as [self-improving-agent](https://clawhub.ai/pskoett/self-improving-agent) — `SKILL.md`, `references/`, `assets/` (templates + optional learnings stubs), `scripts/` (verify, activator, error-detector, extract-skill), `hooks/openclaw/`, optional `_meta.json` after publish.

---

## Purpose

- Point agents at **`public/llm-full.txt`** (full bundle) and **`CLAWHUB.md`** (tribal debugging).
- Document Tempo, MPP/x402, NHS, TIP-20, EVVM, OpenAPI — without duplicating the whole repo.

---

## Zip layout (upload to ClawHub)

Include **everything** below so installers get hooks + scripts:

| Path | Notes |
| --- | --- |
| `SKILL.md` | **Required** — entrypoint |
| `README.md` | This file |
| `_meta.sample.json` | Rename to `_meta.json` after ClawHub assigns IDs (optional) |
| `references/` | All `*.md` |
| `assets/` | `LLM-BUNDLE-SOURCES.md`, `SKILL-TEMPLATE.md`, `templates/`, `learnings/` |
| `scripts/` | `verify-clinical-tempo-context.sh`, `activator.sh`, `error-detector.sh`, `extract-skill.sh` (executable) |
| `hooks/openclaw/` | `HOOK.md`, `handler.js`, `handler.ts` |
| `hooks/README.md` | Hook index |

Do **not** zip `.git` or secrets.

---

## Install (consumers)

### ClawHub site

Use **Install** on [clawhub.ai](https://clawhub.ai/) or the documented CLI, e.g.:

```bash
npx clawhub@latest install arunnadarasa/clinicaltempo
```

(Syntax may vary — follow the live site.)

### From git

```bash
git clone https://github.com/arunnadarasa/clinicaltempo.git
cp -r clinicaltempo/.cursor/skills/clawhub ~/.openclaw/skills/clinicaltempo-clawhub
```

### OpenClaw hook (optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/clinicaltempo-clawhub
openclaw hooks enable clinicaltempo-clawhub
```

### Anyway plugin (optional)

```bash
openclaw plugins install @anyway-sh/anyway-openclaw
```

---

## Maintainer checklist

- [ ] After editing **`scripts/build-llm-full.mjs`** inputs, update **`assets/LLM-BUNDLE-SOURCES.md`**
- [ ] Run **`npm run build:llm`** before release if docs changed
- [ ] Bump **`_meta.sample.json`** version when publishing a new zip
- [ ] Append non-secret incidents to **`CLAWHUB.md`** in the repo

---

## See also

- **`SKILL.md`** — full skill body
- **`references/openclaw-integration.md`** — OpenClaw + ClawHub end-to-end
- **`references/hooks-setup.md`** — Claude Code hook JSON
