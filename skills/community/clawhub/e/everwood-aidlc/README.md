# openclaw-aidlc

OpenClaw port of Everwood **AIDLC** (AI-Driven Development Life Cycle).

Strict human-gated planning (Gates 0–4) before Construction, with a **Gate Deconfliction** reviewer subagent before each human approval. Workspace scratch under `aidlc-sessions/` is the sole content source of truth.

Sibling of [`grok-build-aidlc`](https://github.com/Everwood-Technologies/grok-build-aidlc) (Grok Build / machine-level config). This repo is the **OpenClaw skill package**.

**ClawHub slug:** [`everwood-aidlc`](https://clawhub.ai/mlwood-dev/everwood-aidlc)  
(`openclaw-*` slugs are reserved on ClawHub — do not publish as `openclaw-aidlc`.)

> **Note:** Redis visibility and the Cache State Engine UI were **removed** from this skill (security surface / scope). Planning state is local workspace files only.

## Install

### ClawHub (recommended)

```bash
clawhub install everwood-aidlc

# or via OpenClaw
openclaw skills install everwood-aidlc
openclaw skills install everwood-aidlc --global
```

### From this GitHub repo

```bash
openclaw skills install git:https://github.com/Everwood-Technologies/openclaw-aidlc.git --force

git clone https://github.com/Everwood-Technologies/openclaw-aidlc.git
openclaw skills install ./openclaw-aidlc --force
openclaw skills install ./openclaw-aidlc --global --force
```

Requires `python3` and `bash` only.

## Layout

```text
SKILL.md                 # OpenClaw skill entry (agent instructions)
scripts/                 # session-init, gate-lock
templates/               # gate-0 … gate-4 + gate-deconfliction
references/              # core workflow (incl. deconfliction)
.clawhubignore
```

## Quick use

In chat: `/aidlc` or ask to start AIDLC for non-trivial work.

```bash
python3 scripts/session-init.py --root "$OPENCLAW_WORKSPACE" --objective "…" --json
python3 scripts/gate-lock.py --root "$OPENCLAW_WORKSPACE" --gate gate-0-context \
  --artifact-file path/to/gate.md --status approved
```

Session files land under `$OPENCLAW_WORKSPACE/aidlc-sessions/<uuid>/`. Do not put secrets in gate artifacts.

## Publish to ClawHub

Use slug **`everwood-aidlc`** (not `openclaw-aidlc` — protected namespace).

```bash
npm i -g clawhub
clawhub login
clawhub skill publish . \
  --slug everwood-aidlc \
  --name "Everwood AIDLC (OpenClaw)" \
  --version 1.2.0 \
  --changelog "remove Redis/Cache UI; scratch-only SoT + Gate Deconfliction" \
  --source-repo https://github.com/Everwood-Technologies/openclaw-aidlc \
  --no-input
```

One publish at a time. Avoid parallel `clawhub skill publish` runs (stale upload tickets).

## License

MIT — Everwood Technologies
