# Cruit Candidate Skill

Create and maintain a privacy-respecting Cruit profile for an AI-native developer.

The skill guides a developer through connecting Cruit, choosing approved project folders,
optionally adding a resume, reviewing a profile draft, publishing it, and setting up
weekly refreshes. It is designed for coding agents such as Claude Code, Codex, Cursor,
Amp, and other agents that support `SKILL.md`.

## Install

```sh
curl -fsSL https://cruit.dev/skills/candidate/install.sh | sh
```

For direct marketplace installs, use this folder as the package root.

## Files

- `SKILL.md` — skill entrypoint and offline fallback instructions.
- `INSTRUCTIONS.md` — canonical detailed workflow mirrored from `https://cruit.dev`.
- `install.sh` — user-level installer for supported coding-agent skill folders.
- `SECURITY.md` — privacy and network-access notes.
- `examples/candidate-profile-flow.md` — example user-facing setup flow.

## Safety Model

The skill contacts `https://cruit.dev`, uses browser device auth, and stores user-level
credentials under `~/.cruit/`. It instructs agents not to upload source code, secrets,
`.env` files, private keys, email addresses, phone numbers, street addresses, or private
contact details. The user approves folders before review and approves the profile before
publish.

