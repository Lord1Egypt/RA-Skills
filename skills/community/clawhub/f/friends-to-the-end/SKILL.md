---
name: friends-to-the-end
description: Use when Hermes agents, profiles, or app-embedded agents need to help each other by sharing skills, tools, context, verification, and handoffs. Also triggered by “wanna play” when one Hermes instance should invite another into a task.
version: 1.0.0
author: Hermes Agent + Chucky
license: MIT
metadata:
  hermes:
    tags: [hermes, collaboration, multi-agent, profiles, handoff, community]
    related_skills: [hermes-agent, autonomous-ai-agents, codex, claude-code]
    aliases: [wanna-play, friends-to-the-end]
    suggested_price: community-free
---

# Friends to the End / Wanna Play

## Overview

Use this skill when one Hermes profile, service, dashboard, or embedded workflow needs a structured handoff to another Hermes-capable profile. The goal is to make profile-to-profile collaboration safe, truthful, and verifiable: provide only the necessary context, use the right profile/tools/skills, request machine-readable results when useful, and verify real side effects before claiming success.

The trigger phrase “wanna play” means: ask another capable Hermes profile or service to participate in the task with a clear role and verifiable return value.

This skill is especially useful when an app has weaker local logic than a full Hermes profile. Example: a web app can do OCR, but a Hermes profile has vision tools and a domain skill, so the app calls Hermes as a fallback and then verifies the result against source APIs.

## When to Use

Use this skill when:

- A Hermes-powered app needs a stronger Hermes profile for fallback reasoning.
- One profile has a skill/tool another profile does not.
- You need to clone or create a dedicated profile for an app, child agent, worker, or friend.
- A task crosses systems: dashboard + VM + Designer/ComfyUI + Codex/llama.cpp + web/vision.
- The user asks for Chucky, Pokémon, Matthew, Designer, or another named agent/profile to work together.
- The user says “wanna play”, “work with Chucky”, “let the agents help each other”, or similar.

Do not use this skill for:

- Simple single-agent tasks that need no other profile/tool context.
- Sharing secrets between agents without explicit need.
- Claiming another agent completed work without verifying its output.

## Core Pattern

1. Identify the friend.
   - Which profile/service has the needed tools or skills?
   - Which host is it on?
   - Which profile name should be used?
   - Is the profile dedicated to the app, or are you borrowing a general profile temporarily?

2. Verify live state.
   - List profiles: `hermes profile list`.
   - Check toolsets: `hermes tools list --profile <profile>`.
   - Check skill files or skill list.
   - Check service env if an app launches Hermes.
   - Check network endpoints for external helpers.

3. Prefer a dedicated profile for app embeddings.
   - Clone from the working profile if needed:
     `hermes profile create <new-profile> --clone-from <known-good-profile> --clone-all`
   - Switch the app/service to explicit env vars:
     `APP_HERMES_PROFILE=<new-profile>`
     `APP_HERMES_HOME=/root/.hermes/profiles/<new-profile>`
   - Keep secrets in the Hermes profile, not in app code.

4. Pass a compact, self-contained prompt.
   - Include the artifact path or URL.
   - Include OCR/logs/source hints, but tell the friend not to trust filenames.
   - Request strict JSON for app integrations.
   - Ask for confidence and reason when identification is uncertain.

5. Verify the friend’s answer.
   - If the friend identifies an object/card/service, validate it against an authoritative source API.
   - If the friend writes a file, read it back.
   - If the friend starts a service, check health endpoints.
   - If the friend claims a price/value, show the source and distinguish estimates from raw market data.

6. Clean up temporary artifacts.
   - Delete test cards/uploads if they were only verification.
   - Remove stale active work from Kanban if it is no longer active.
   - Keep backups for code/config changes.

## Example: App Calls Hermes as a Vision Fallback

A web app can launch Hermes only after cheap local methods fail:

```bash
HERMES_HOME=/root/.hermes/profiles/pokemon \
hermes chat -Q \
  --profile pokemon \
  --skills trading-card-identification-pricing \
  --toolsets vision,web \
  -q 'Identify the Pokémon card in /path/to/upload.jpg. Use vision, not filename. Return compact JSON only.'
```

Good JSON shape:

```json
{
  "card_name": "Perrin",
  "set_number": "220/167",
  "set_name": "Twilight Masquerade",
  "rarity": "Special Illustration Rare",
  "confidence": 0.96,
  "reason": "Visible Supporter name and bottom set number match source data."
}
```

Then the app should query a source API using the returned `card_name` and `set_number`, not blindly trust the model result.

## Profile Hygiene

For embedded apps, avoid long-term dependency on a personal profile name if the app is its own agent. Create a dedicated profile:

```bash
hermes profile create pokemon --clone-from chucky --clone-all
```

Then configure the service with explicit environment variables, for example systemd drop-in:

```ini
[Service]
Environment=APP_HERMES_PROFILE=<dedicated-profile>
Environment=APP_HERMES_HOME=/root/.hermes/profiles/<dedicated-profile>
Environment=APP_HELPER_IMAGE_URL=<internal-image-helper-url>
Environment=APP_HELPER_CODE_URL=<internal-code-helper-url>
Environment=HERMES_NO_UPDATE_CHECK=1
```

Reload and restart:

```bash
systemctl daemon-reload
systemctl restart <service>
systemctl show <service> -p Environment --no-pager
```

## Community and Pricing Notes

Default community posture: share this skill freely under MIT unless the user or registry explicitly supports paid skills.

If a future Hermes skill marketplace supports paid listings, treat this as a standard utility/community skill and use a modest “standard” listing price rather than premium pricing. Suggested baseline: free for community registry; if paid listing metadata is required, use a low standard utility price such as USD $5, not a subscription or enterprise price.

Do not invent a sale/publishing result. Use `hermes skills publish` or the current registry workflow and report the exact URL, package ID, or blocker.

## Common Pitfalls

1. Confusing app name with Hermes profile name.
   - “Pokemon” might be the app, service, or profile. Verify with `hermes profile list` and service env.

2. Borrowing a personal profile forever.
   - It works for a quick test, but app integrations should get a dedicated profile.

3. Trusting filenames.
   - For images/cards/documents, filenames are user-supplied hints at best. Use image/OCR/source matching.

4. Claiming a friend succeeded without verification.
   - Hermes child runs and spawned profiles can fail silently, timeout, or return plausible wrong answers. Verify externally.

5. Leaking secrets between friends.
   - Keep API keys in profile `.env` files. Never print or copy secret values into prompts, logs, or skills.

6. Overusing expensive tools.
   - Try cheap deterministic checks first: OCR, source APIs, local health checks. Use vision/LLM fallback when those fail.

## Verification Checklist

- [ ] The intended profile exists and is the one the app/service invokes.
- [ ] Required toolsets are enabled for that profile.
- [ ] Required skills are installed for that profile.
- [ ] Service environment explicitly names the profile/home when embedded.
- [ ] The friend returns structured output for app integrations.
- [ ] The result is verified against live files, APIs, logs, browser behavior, or source data.
- [ ] Temporary test artifacts are cleaned up.
- [ ] Any community publish/share attempt reports a real handle or exact blocker.
