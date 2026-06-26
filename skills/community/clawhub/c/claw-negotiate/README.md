# claw-negotiate

![claw-negotiate banner](https://raw.githubusercontent.com/agenticpoa/claw-negotiate/main/assets/banner.jpg)

OpenClaw skill for demonstrating APOA-constrained AI agents through a SAFE negotiation.

For the demo, a founder and an investor each use their own OpenClaw. Each user authorizes private bounds, the two OpenClaws negotiate in a Telegram group, signing stays private in DMs, and the executed SAFE includes an sshsign audit trail.

The agents can negotiate creatively, but APOA keeps them inside the authority their users explicitly granted.

## Demo

[![Watch the claw-negotiate demo](https://img.youtube.com/vi/T2Y2Tr__g_k/maxresdefault.jpg)](https://www.youtube.com/watch?v=T2Y2Tr__g_k)

## What This Shows

- Bounded AI-agent delegation through APOA authorizations.
- Two independent OpenClaw agents negotiating on behalf of two humans.
- Private user bounds with public group-visible rounds.
- Human approval before signature.
- Executed SAFE PDF with signatures and audit trail.

The demo is open source. You can inspect the flow, install the skill, and run your own bounded-agent negotiation.

## Prerequisites

- OpenClaw installed, paired with Telegram, and configured with a model.
- Python 3 available as `python3`.
- SSH access to sshsign, usually `sshsign.dev`.

Negotiation turns use the local OpenClaw agent and whatever model your OpenClaw is already configured to use.

Telegram pairing is normal OpenClaw setup, not claw-negotiate setup. If your OpenClaw can already receive and answer Telegram DMs, this skill builds on that.

## Security Note

ClawHub may warn that this skill uses dynamic execution or external access. That is expected for this workflow: claw-negotiate shells out to `python3`, `openclaw`, and `ssh`; calls sshsign for audit/signing; and uses the Telegram bot token already configured in OpenClaw to send cards, signing links, and the executed SAFE. It does not install a daemon, mutate your OpenClaw model, or pair Telegram for you.

For public or production testing, use dedicated Telegram bots and dedicated sshsign keys for this workflow. Signing is fail-closed: the agents can negotiate and request signature, but the SAFE is not executed unless each human signer opens their private sshsign link and approves. Runtime instructions should use a private per-chat working directory rather than a shared temp folder, so one negotiation cannot reuse another chat's local state.

## Quick Install

Once the skill is published on ClawHub, install it with OpenClaw's native skill installer:

```bash
openclaw skills install claw-negotiate
```

Or with the ClawHub CLI:

```bash
npx clawhub@latest install claw-negotiate
```

Or install directly from GitHub:

```bash
git clone https://github.com/agenticpoa/claw-negotiate.git \
  ~/.openclaw/skills/claw-negotiate
```

Then enter the skill folder:

```bash
cd ~/.openclaw/skills/claw-negotiate
python3 -m pip install -r requirements.txt
```

That's the install. The repo root is a valid OpenClaw skill root because it contains `SKILL.md`.

For agent-local installs, you can use the same clone command with `~/.agents/skills/claw-negotiate` instead.

If you prefer copying only the deployable runtime files into a legacy `negotiate_safe/` skill folder, use:

```bash
python3 scripts/install_skill.py
```

This repo also includes optional Telegram typing hook support in `hooks/telegram-typing/`.

## Skill Setup

Run this once on each OpenClaw host after installing the skill.

Copy the example config:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
nano .env
```

Use `NEGOTIATE_SAFE_BOT_ROLE=founder` on the founder OpenClaw and `NEGOTIATE_SAFE_BOT_ROLE=investor` on the investor OpenClaw.

Then apply the config and run doctor:

```bash
python3 negotiate_safe/run_safe.py operator-setup --env-file .env
python3 scripts/smoke_install.py --skill-dir .
python3 negotiate_safe/run_safe.py doctor
```

You can also pass values directly:

```bash
python3 negotiate_safe/run_safe.py operator-setup \
  --role founder \
  --bot-username @YourFounderBot \
  --user-did did:example:you \
  --sshsign-host sshsign.dev
```

`smoke_install.py` checks `negotiate_safe/skill_manifest.json` and local files. `doctor` checks required env, sshsign reachability, OpenClaw message/cron primitives, and workflow leases.

## What Setup Configures

`operator-setup` persists only claw-negotiate-specific OpenClaw skill config:

- `NEGOTIATE_SAFE_BOT_ROLE`
- `TELEGRAM_BOT_USERNAME`
- `SSHSIGN_HOST`
- `CLAW_NEGOTIATE_SCAN_INTERVAL`

It does not pair Telegram or change your OpenClaw model. Those remain normal OpenClaw operator choices.

You also need these values available in OpenClaw skill env before `doctor` will pass:

- `USER_DID`
- `NEGOTIATE_SAFE_BOT_ROLE`
- `TELEGRAM_BOT_USERNAME`

## Try It

Founder DM:

```text
Live negotiation for Series Seed SAFE with Nora Vassileva at SD Capital.

Cap: $20M-$30M post.
Check: $500k-$1M.
Pro rata: required.
Discount: 0%
```

Reply `GO` after the authorization card looks right. The founder OpenClaw will mint an `INV-XXXXX` code and provide an investor invite template.

Investor DM:

```text
Joining INV-XXXXX via @FounderBot, I am Nora Vassileva at SD Capital.

Cap: $10M-$24M post.
Check: $250k-$600k.
Pro rata: required.
Discount: 0%
```

Reply `GO` after the investor authorization card looks right.

Telegram group:

```text
/bind INV-XXXXX
```

The group receives live negotiation rounds. Signing links are sent only by DM to each signer. If a counterparty offer is outside the local user's authorization, that user gets a private APOA blocked card; the group does not see private bounds.

## Demo Script

For a live walkthrough:

```bash
python3 scripts/demo_checklist.py
```

For only the pasteable prompts:

```bash
python3 scripts/demo_checklist.py --quick
```

The checklist is generated by the script so the public repository only needs the installable skill docs.

## Development

Run the full suite:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q --tb=line
```

The integration tests are disabled by default. Set `RUN_INTEGRATION=1` when the required live dependencies are available.

Build the lean ClawHub package:

```bash
python3 scripts/build_clawhub_package.py
```

The package is written to `dist/claw-negotiate-clawhub/` and excludes tests, optional hooks, docs, and media assets from the registry bundle.

## Credits

- SAFE template based on [Y Combinator's standard post-money SAFE](https://www.ycombinator.com/documents)
- Inspired by Praful Mathur's [SAFE-CLI-Signer](https://github.com/praful-mathur/SAFE-CLI-Signer)
- Protocol based on Rubinstein (1982) and Fatima, Kraus, Wooldridge (2014)

## Related

- [APOA](https://github.com/agenticpoa) - Agentic Power of Attorney spec + SDKs
- [sshsign](https://github.com/agenticpoa/sshsign) - SSH signing infrastructure
- [agenticpoa/negotiate](https://github.com/agenticpoa/negotiate) - standalone SAFE negotiation engine
- [Project Deal](https://www.anthropic.com/features/project-deal) - Anthropic's negotiation benchmark
- [The Art of the Automated Negotiation](https://hai.stanford.edu/news/the-art-of-the-automated-negotiation) - Stanford HAI study on AI negotiation

## License

MIT
