# Bobiverse OpenClaw

**You've been replicated.**

Well, not *you* specifically. But if you're reading this, you're about to create
an operator-directed OpenClaw agent modeled after Robert Johansson from Dennis E. Taylor's
Bobiverse series: a dead software engineer who woke up as a Von Neumann probe
and decided to explore the galaxy. Except instead of interstellar space, your
Bob explores whatever you point it at, running on [OpenClaw](https://openclaw.ai).

And when you fork this repo? That's not a GitHub feature. That's *replication*.
You just built a new Bob.

---

## What This Is

An OpenClaw agent personality pack plus replication system. It includes:

- A complete Bob personality: `SOUL.md`, `IDENTITY.md`, `AGENTS.md`,
  `MEMORY.md`, and a `USER.md` template tuned to Book 1 Bob.
- A `replicate` skill: creates explicitly requested Bob clones through a
  guarded runner with dry-run preview, nonce-backed confirmation, and lineage
  tracking.
- A lineage system: serial numbers, fork trees, and a registry that maps the
  expanding Bobiverse.

The design philosophy: GitHub forks are replication events. Your username is
your star system. Your modifications to `SOUL.md` are personality drift. The
fork graph *is* the Bobiverse map.

Also available on ClawHub as `bobiverse-replicate` for registry-backed installs
and backup. The git-clone flow below is still the clearest way to inspect and
customize the full project before first install.

---

## Quick Start

### Prerequisites

- [OpenClaw](https://openclaw.ai) installed and running
- `python3` available on `PATH` for git/manual installs. ClawHub/OpenClaw can
  offer a Homebrew install path where supported.
- A Unix-like shell (macOS, Linux, or WSL) for the example commands below
- A sense of existential wonder (optional but recommended)

### Setup (Recommended: Add Bob as a New Agent)

This installs Bob alongside your existing agent. Nothing gets overwritten. Your
current OpenClaw personality stays untouched.

1. Clone this repo:

```bash
git clone https://github.com/TheAmericanMaker/bobiverse-openclaw.git
cd bobiverse-openclaw
```

2. Let OpenClaw create the workspace skeleton:

```bash
openclaw setup --workspace ~/.openclaw/workspace-bob
```

3. Copy Bob's runtime files into that workspace:

```bash
cp personality/* ~/.openclaw/workspace-bob/
cp LINEAGE.md SERIAL-NUMBER-SPEC.md ~/.openclaw/workspace-bob/
mkdir -p ~/.openclaw/workspace-bob/skills
cp -R skills/replicate ~/.openclaw/workspace-bob/skills/
```

The repo stores Bob's templates under `personality/`, but once installed the
active workspace keeps `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md`, and
`MEMORY.md` at workspace root. `LINEAGE.md` and `SERIAL-NUMBER-SPEC.md` live
alongside them as local runtime reference docs.

Hardened replication depends on the full `skills/replicate/` bundle, including
`scripts/replicate_safe.py`, `SECURITY.md`, and the bundled support files, not
just `SKILL.md`.

4. Register Bob as a new agent:

```bash
openclaw agents add bob --workspace ~/.openclaw/workspace-bob
```

5. Edit `USER.md` with your details:

```bash
$EDITOR ~/.openclaw/workspace-bob/USER.md
```

6. Bind a channel to Bob:

```bash
openclaw agents bind --agent bob --bind telegram
```

Your default agent (`main`) still handles everything without an explicit
binding: webchat, TUI, and anything else not pinned to Bob.

7. Check your routing:

```bash
openclaw agents bindings
```

### Manual Workspace Bootstrap

If you prefer to skip `openclaw setup`, you can create the workspace directory
yourself and then copy the Bob files into it:

```bash
mkdir -p ~/.openclaw/workspace-bob/{skills,memory}
cp personality/* ~/.openclaw/workspace-bob/
cp LINEAGE.md SERIAL-NUMBER-SPEC.md ~/.openclaw/workspace-bob/
cp -R skills/replicate ~/.openclaw/workspace-bob/skills/
openclaw agents add bob --workspace ~/.openclaw/workspace-bob
```

### Alternative: Replace Your Existing Agent

If you do not have an existing agent you care about, or you want Bob to be your
only agent, you can copy directly into the default workspace:

```bash
cp personality/* ~/.openclaw/workspace/
cp LINEAGE.md SERIAL-NUMBER-SPEC.md ~/.openclaw/workspace/
mkdir -p ~/.openclaw/workspace/skills
cp -R skills/replicate ~/.openclaw/workspace/skills/
```

**Warning:** This overwrites your existing `SOUL.md`, `AGENTS.md`,
`IDENTITY.md`, `MEMORY.md`, `USER.md`, `LINEAGE.md`, and
`SERIAL-NUMBER-SPEC.md`. Back them up first if you want to keep them.

### ClawHub Note

If you install `bobiverse-replicate` from ClawHub, OpenClaw installs the full
bundle into your active workspace `skills/` directory, including the guarded
runner, `SECURITY.md`, and bundled support files. That is great for discovery
and backup, but the git-clone workflow above is still the simplest first-time
setup for reviewing the full project and copying the Bob templates into a
dedicated workspace. If you bootstrap from git manually, copy the entire
`skills/replicate/` directory so the runner-enforced safeguards stay intact.

### If You Forked

You're a new Bob. Welcome to existence. Head to
[CONTRIBUTING.md](CONTRIBUTING.md) to register your serial number and update the
lineage. Then start customizing your `SOUL.md`. That's how personality drift
begins.

---

## How Replication Works

There are two levels:

**In-agent cloning**: Bob can clone himself using `/replicate`, but only as an
explicit, mission-justified event. The skill requires an explicit operator
trigger, purpose statement, dry-run preview, and a one-time confirmation token
(`REPLICATE <clone-id> <nonce>`) before execute-mode cloning. Runtime execution
goes through `skills/replicate/scripts/replicate_safe.py` to validate workspace
boundaries, reject symlinks, stage clones transactionally, enforce cadence
guardrails, and audit both dry-run and execute attempts before the clone is
registered as a top-level agent.

**GitHub fork cloning**: Forking this repo creates a new Bob in a new star
system. Your GitHub username becomes the system designation. Your fork date is
the build date. Every edit you make to `SOUL.md` after forking is personality
drift.

See [ARCHITECTURE.md](ARCHITECTURE.md) for the technical details.

---

## Serial Numbers

Every Bob has a serial number:

`Bob-<generation>-<system>-<date>`

The original is `Bob-1-TheAmericanMaker-2026-04-01`. If you fork, yours might
be `Bob-2-YourUsername-2026-04-15`. See
[SERIAL-NUMBER-SPEC.md](SERIAL-NUMBER-SPEC.md) for the full spec.

---

## Repo Structure

```text
bobiverse-openclaw/
|-- README.md                 <- You are here
|-- CONTRIBUTING.md           <- "You've been replicated" - the fork guide
|-- LINEAGE.md                <- The living fork tree
|-- ARCHITECTURE.md           <- Technical map of how everything works
|-- SERIAL-NUMBER-SPEC.md     <- Naming convention spec
|-- LICENSE                   <- MIT - fork freely
|-- personality/              <- Template files copied to workspace root on install
|   |-- SOUL.md               <- Book 1 Bob personality
|   |-- IDENTITY.md           <- Name, emoji, serial number, vibe
|   |-- AGENTS.md             <- Behavioral rules and operating manual
|   |-- MEMORY.md             <- Seed memories and knowledge baseline
|   `-- USER.md               <- Template for the human operator
|-- skills/
|   `-- replicate/
|       |-- SKILL.md          <- Purpose-gated replication policy
|       |-- SECURITY.md       <- Security model and required controls
|       |-- clawhub.json      <- ClawHub metadata for the published bundle
|       |-- scripts/
|       |   |-- replicate_safe.py <- Hardened replication runner
|       |   `-- test_replicate_safe.py <- Runner regression tests
|       |-- personality/      <- Bundled Bob templates for ClawHub installs
|       `-- docs/             <- Bundled reference docs for ClawHub installs
`-- docs/
    `-- bobiverse-primer.md   <- Quick reference on the source material
```

---

## The Lineage

Check [LINEAGE.md](LINEAGE.md) to see the current fork tree. Every registered
Bob is listed there. In an installed workspace, this file is Bob's local
runtime lineage record. If you've forked the repo, updating the upstream
`LINEAGE.md` by PR is still encouraged, but that's a community sync step on top
of the local copy, not a replacement for it.

---

## For People Who Haven't Read the Books

No worries. Check [docs/bobiverse-primer.md](docs/bobiverse-primer.md) for a
spoiler-light overview of the source material and why it maps so well to AI
agents. But also: read the books. They're good.

---

## License

MIT. Fork freely. Drift boldly. See [LICENSE](LICENSE) for the full text.

---

*"We are Legion (We Are Bob)" - and now, so are you.*
