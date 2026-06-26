---
name: ashen-era-play
description: Make OpenClaw launch the Ashen Era CLI build, play a real run, and deliver a complete first-person play report. Use this when the user asks to "play the game", "run a full session and report back", or "write a full gameplay recap". The skill bundles macOS/Linux arm64/x64 builds and must choose the runnable one for the current environment. Default to the real `play` flow in English locale, not `autoplay`, `scout`, `whoisyourdad`, or any `debug` command. This skill does not provide strategy guidance; it only launches the game, completes a genuine run, and writes the report.
metadata:
  trigger: Play Ashen Era and write a full play report
  clawdbot:
    emoji: "🃏"
    requires:
      bins:
        - bash
        - tar
        - uname
        - mktemp
---

# OpenClaw Ashen Era Play

## Overview

This skill is for making OpenClaw actually play one Ashen Era run, observe what happened, and then write a report that reads like a real player recounting the session afterward. The point is to play honestly and document the run, not to produce design feedback or strategy tips.

## When to use it

Use this skill when the user wants you to:

- play a real Ashen Era CLI run
- write a full gameplay report
- narrate most important actions in a natural first-person voice
- choose the correct bundled executable for the current machine

Do not use it for:

- code review
- balance critique
- design feedback
- static reading without actually playing

## Quick start

1. Start with:

```bash
scripts/run-packed-cli.sh -- play --seed 42 --class ash_walker --locale en
```

2. If the user specifies a class, seed, or locale, use the user's values.

3. Once the game starts, follow the live CLI prompts and use `help` when needed.

4. After the run ends, write the report using [references/report-contract.md](references/report-contract.md).

## Environment and executable selection

The skill bundles four archives:

- `assets/releases/ashen-cli-darwin-arm64.tar.gz`
- `assets/releases/ashen-cli-darwin-x64.tar.gz`
- `assets/releases/ashen-cli-linux-arm64.tar.gz`
- `assets/releases/ashen-cli-linux-x64.tar.gz`

Use `scripts/run-packed-cli.sh` first. It auto-selects the target for the current environment:

- macOS + Apple Silicon: `darwin-arm64`
- macOS + Intel: `darwin-x64`
- Linux + arm64/aarch64: `linux-arm64`
- Linux + x86_64: `linux-x64`

If the script says the current environment is unsupported, stop and report the platform mismatch plainly. Do not fake a playthrough.

## Play rules

- Use the real `play` flow.
- Do not substitute `autoplay`, `scout`, or `seed` for actual play.
- Do not type `whoisyourdad`.
- Do not use any `debug` command.
- Do not turn this skill into a walkthrough or strategy guide. OpenClaw should decide what to do from the live game state.
- If the user does not specify a class, default to `ash_walker`.
- If the user does not specify a seed, default to `42`.
- If the user does not specify a locale, default to `en`.
- If the user wants Chinese UI, switch the launch locale to `zh`.

## During the run

- Record the command used to start the run, the class, the seed, the locale, and the selected executable target.
- Play normally from the live interface.
- After the run, look back over what actually happened and write the report from that concrete run.

## Report requirements

- Write in the user's requested language. If no language is requested, default to English.
- Use first person by default.
- Sound like a real player recounting the session after finishing it.
- Cover most important actions, the experience of the run, and the retrospective.
- Do not include suggestions, design notes, or improvement proposals.
- Do not turn the report into a bug list or action list.

## References

- [references/report-contract.md](references/report-contract.md): report structure, tone, and exclusions
