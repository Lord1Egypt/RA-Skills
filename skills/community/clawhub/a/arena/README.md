# Arena

**Give a hard problem several independent attempts, then ship one checked result.**

Arena is a Codex skill for substantial tasks with more than one plausible solution. It gives multiple agents the same brief, compares their work against a rubric, combines the strongest ideas, and verifies the final deliverable. Candidates work in separate locations so their attempts stay independent.

Use it for architecture choices, tricky refactors, competing implementations, or a draft where you want several approaches before committing to one. A request such as `$arena Design and implement a cache invalidation strategy for this service` is enough to start. Arena is usually unnecessary for a small, straightforward edit.

## What happens

1. Codex defines the deliverable, acceptance criteria, and a short rubric.
2. Independent candidates work on the same task in separate locations.
3. A judge compares the candidates when an agent slot is available; Codex also reviews every result directly.
4. Codex integrates the best solution, verifies it, and reports what was chosen and why.

The number of candidates depends on your request and the available agent slots. If parallel agents are unavailable, Arena reports that limit and proceeds with a single result or asks how to continue. Running multiple agents can take longer and use more model calls than an ordinary task.

## Install

You need Codex, Git, Bash, and an empty `arena` skill directory. Clone the repository into your Codex skills folder:

```sh
git clone https://github.com/yagel-yosef/arena-skill.git "${CODEX_HOME:-$HOME/.codex}/skills/arena"
```

Then ask Codex to `arena` a substantial task or invoke `$arena` explicitly.

## Updates

Each Arena invocation asks Codex to run `scripts/update.sh` before starting the task. The script fetches the latest `main` commit from this repository, and Codex rereads `SKILL.md` if it changed. There is no background updater.

For a Git installation, the updater requires the expected GitHub origin, a clean checkout on `main`, and a fast-forward update. A ClawHub installation has no Git checkout; the updater fetches the repository and replaces Arena's `SKILL.md`, README, and updater script with the latest copies. Local edits to those three files in a ClawHub installation will be replaced. If an update fails, Arena tells you and uses the installed version. For a Git installation, you can see its revision with:

```sh
git -C "${CODEX_HOME:-$HOME/.codex}/skills/arena" rev-parse --short HEAD
```

Updates can change both Arena's instructions and its scripts. They come from the repository's `main` branch without separate approval of each commit. Review that branch if you rely on automatic updates; a checkout pinned to a commit will refuse the updater and continue using its installed instructions.
