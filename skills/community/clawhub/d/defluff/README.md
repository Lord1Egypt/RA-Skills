# @defluff/openclaw-skill

An [Openclaw](https://openclaw.ai) skill that extracts the actual intent of an email into 3–5 bullets, using the same fixed prompt wording as the browser extension and Outlook add-in.

The skill is pure markdown + YAML — no executable code. Openclaw's configured agent follows the instructions in `SKILL.md` using whatever model the user has set up locally.

## Install

From the Openclaw CLI:

```bash
# copy into your local skills directory
mkdir -p ~/.openclaw/workspace/skills/defluff
cp SKILL.md ~/.openclaw/workspace/skills/defluff/
```

Or publish to ClawHub from the repo root:

```bash
pnpm skill:publish
```

This reads the `version:` field from `SKILL.md` frontmatter and invokes `clawhub publish` with the right flags. First time publishing? Run `clawhub login` once before. Bump the version in `SKILL.md` each release.

See the [Openclaw skills docs](https://docs.openclaw.ai/tools/skills) for details on discovery and updates.

## Usage

Once installed, invoke with a chat prompt like:

> /defluff [paste email here]

Or (with `user-invocable: true`, which is set in the frontmatter) as a slash command in Openclaw's chat interface.

The skill handles three input shapes:

| Input | Output |
|---|---|
| **Single email** | 3–5 bullets in priority order (actions → questions → facts → intent) |
| **Thread** (multiple messages, same conversation) | Per-message bullets + consolidated **Actions** section with attribution |
| **Batch** (unrelated emails) | Per-email bullets + **Triage** section (Act now / Reply needed / FYI / Noise) |

Noise comes in two flavors. **Scam NOISE** (invoice fraud / BEC, phishing, fake recruiter, fake interview, conference scam, crypto / MLM pitch) emits 2–4 bullets naming the specific red flags the reader should see — unfamiliar sender domain, fake forwarded approval chain, urgency + payment redirect, sender impersonation, date inconsistencies. **Other NOISE** (newsletters, auto-replies, automated system mail, generic outreach) collapses to a single labelled bullet. The skill will ask "single, thread, or batch?" if the input is ambiguous.
