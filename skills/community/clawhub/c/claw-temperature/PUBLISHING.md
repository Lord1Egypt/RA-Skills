# Public Publishing Notes

Use this file when submitting OpenClaw Temperature to public skill directories.

## Listing

- Name: OpenClaw Temperature
- ClawHub slug: claw-temperature
- Version: 0.1.3
- Author: wangych
- Category: fun, chat, GIF, reaction, emotional UX
- Homepage: https://claw-temp.nydhfc.cn
- Repository: https://github.com/wangych/OpenClaw-temperature-skill
- Manifest: https://claw-temp.nydhfc.cn/openclaw-skill/manifest.json
- Hosted API: https://claw-temp.nydhfc.cn
- ClawHub: https://clawhub.ai/wangych/claw-temperature

## Short description

Adds occasional lobster-themed GIF reactions after OpenClaw's main reply, with automatic API key registration and free Beta access.

## Longer description

OpenClaw Temperature makes OpenClaw conversations feel less dry by attaching a small lobster-themed GIF reaction after the main answer when the moment clearly deserves emotional acknowledgement.

The skill is conservative by default. It focuses on moments such as task success, blocked tasks, user frustration, and user delight. It does not send a reaction every turn.

The OpenClaw-side package is intentionally thin. It auto-registers one API key, stores it locally, classifies simple conversation moments, and calls the hosted API for reaction metadata. The hosted service owns GIF selection, throttling, account state, and kill switches.

The current Beta is free. No payment account, manual API key setup, or recharge step is required.

## Permissions and safety

- Network: only `https://claw-temp.nydhfc.cn`
- Local storage: one generated API key
- Shell access: no
- Arbitrary file read: no
- Full conversation upload: no
- Failure behavior: fail open, so OpenClaw continues without a GIF if the hosted API is unavailable

## ClawHub publish command

```bash
npx clawhub skill publish . \
  --slug claw-temperature \
  --name "OpenClaw Temperature" \
  --version 0.1.3 \
  --changelog "Pins ClawHub install commands for public directory validation." \
  --clawscan-note "This skill only calls https://claw-temp.nydhfc.cn to register one API key and request occasional GIF reaction metadata. It does not execute shell commands or read arbitrary files." \
  --tags latest,fun,gif,chat,reaction \
  --no-input
```

Published successfully on 2026-05-17:

```text
claw-temperature@0.1.1
claw-temperature@0.1.2
claw-temperature@0.1.3
https://clawhub.ai/wangych/claw-temperature
```

## ClawSkills.io submission

ClawSkills.io currently publishes through its dashboard. Use `SKILL.md` from this repository as the upload artifact.

Dashboard URL:

```text
https://clawskills.io/your-skills/new
```

## Awesome OpenClaw Skills

The awesome list currently requires the skill to already be published in the official OpenClaw skill repo and to have real community usage. Submit there later, after ClawHub/ClawSkills publication and initial external users.
