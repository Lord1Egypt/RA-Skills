# Hermes Agent Adapter

## Overview

[Hermes Agent](https://hermes-agent.nousresearch.com/) (Nous Research) uses the same
workspace file conventions this skill manages: `SOUL.md` for the persona,
`MEMORY.md` / `USER.md` for memories, and `AGENTS.md` for workspace instructions.
Hermes even ships an OpenClaw migration importer, so Soul packages work in a Hermes
workspace **without format conversion** — installing a soul is a matter of placing
the Soul Spec files where Hermes reads them.

## Installing this skill in Hermes

Hermes supports the [agentskills.io](https://agentskills.io) open format this skill
follows. Any of these works:

```bash
# from a URL
hermes skills install https://raw.githubusercontent.com/clawsouls/clawsouls-skill/main/SKILL.md

# or clone into the skills directory
git clone https://github.com/clawsouls/clawsouls-skill ~/.hermes/skills/clawsouls
```

Then invoke it as `/clawsouls` or just ask: *"install a soul"*.

## Using souls in a Hermes workspace

1. `cd` into the Hermes workspace (the directory containing `SOUL.md` / `AGENTS.md`).
2. Run the usual commands — `npx clawsouls install <owner/name>`, `npx clawsouls use <owner/name>`.
   The CLI writes persona files (`SOUL.md`, `IDENTITY.md`, `AGENTS.md`, `HEARTBEAT.md`,
   `STYLE.md`) into the current workspace and backs up what was there.
3. `MEMORY.md` and `USER.md` are never overwritten — your Hermes memories survive
   persona switches (the persona/memory boundary is a Soul Spec design rule).
4. Restart the Hermes session and start a new chat so the previous persona's
   conversation context doesn't linger.

`npx clawsouls soulscan` works the same way — point it at the Hermes workspace to
verify persona integrity and scan for the 53 safety patterns after any install.

## Status / roadmap

- **Works today**: manual placement (run commands inside the Hermes workspace, step 2
  above), `soulscan`, `checkpoint`, `export system-prompt`.
- **Planned**: first-class `--platform hermes` detection in the `clawsouls` CLI so
  `platform`/`detect` reports Hermes workspaces automatically, matching the ZeroClaw
  adapter approach (see `ZEROCLAW_ADAPTER.md`).

Issues and reports: https://github.com/clawsouls/clawsouls-skill/issues
