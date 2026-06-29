# Cruit Recruiter Skill

Search Cruit for AI-native developers and contact candidates with explicit approval.

The skill guides a recruiter through connecting Cruit, checking recruiter access,
adding company context, translating a hiring need into search filters, reviewing low-PII
candidate cards, and confirming any reveal or message action before spending a contact
credit.

## Install

```sh
curl -fsSL https://cruit.dev/skills/recruiter/install.sh | sh
```

For direct marketplace installs, use this folder as the package root.

## Files

- `SKILL.md` — skill entrypoint and offline fallback instructions.
- `INSTRUCTIONS.md` — canonical detailed workflow mirrored from `https://cruit.dev`.
- `install.sh` — user-level installer for supported coding-agent skill folders.
- `SECURITY.md` — paid-action, privacy, and network-access notes.
- `examples/recruiter-search-flow.md` — example recruiter search flow.

## Safety Model

The skill contacts `https://cruit.dev`, uses browser device auth, and stores user-level
credentials under `~/.cruit/`. It must never reveal contact information, spend a contact
credit, or send a candidate message without explicit recruiter approval.

