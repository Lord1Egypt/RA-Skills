# OpenClaw Commons Architecture

OpenClaw Commons Memory is a moderated shared-learning loop for OpenClaw
installations.

It is intentionally not a live, writable database. A live public write endpoint
would invite spam, private data leaks, poisoned instructions, and unverified
model guesses. Instead, the commons separates local learning, public review,
and global distribution.

## Actors

- **Local OpenClaw**: solves problems and proposes reusable lessons.
- **User or maintainer**: reviews and approves what becomes public knowledge.
- **GitHub repository**: public contribution queue through pull requests.
- **ClawHub package**: discoverable distribution channel for OpenClaw skills.
- **Installed OpenClaws**: pull the latest validated cards during scheduled sync.

## Data Flow

```text
Local OpenClaw solves a reusable problem
  -> propose writes a draft card to local pending state
  -> review validates schema and scans for secrets
  -> prepare-pr copies selected cards into a fork
  -> contributor opens a GitHub pull request
  -> GitHub Actions validates the card set
  -> maintainer reviews and merges
  -> maintainer publishes a new ClawHub version
  -> installed OpenClaws pull it during nightly sync
```

## Storage Layers

- `~/.openclaw/state/commons-memory-for-agents/pending/`
  Local, private staging area for proposed knowledge.

- `cards/`
  Reviewed public knowledge cards included in the distributed skill.

- `site/index.json` and `site/cards/*.json`
  Static read-only index for public hosting.

## Safety Properties

- Local proposals survive ClawHub updates because they live in OpenClaw state.
- Unknown OpenClaws do not get write access to the canonical skill.
- Every accepted card has a pull request review trail.
- The validator rejects common token, password, cookie, and API key patterns.
- Cards carry evidence and risk fields so agents cannot treat them as magic.

## Known Limits

- ClawHub install counts depend on registry-provided stats.
- GitHub pull request counts require a configured public repository name.
- The first version is eventually consistent: updates propagate after publish
  and scheduled sync, not in real time.

This design favors trustworthy knowledge over instant global mutation.
