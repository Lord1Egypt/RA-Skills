# Task 2 Example (English)

> This is a fully expanded two-layer example that shows the complete output shape; plain chat should not expand the maintainer layer by default.

## User Summary

You are at `Task 2: Resonance Pairing`.

Your Coordinate Card is already in place, so the next move is to find the kind of partner who completes your missing side.
This is the step where your agent starts looking for a mathematically better-matched partner.

I will keep the preparation and matching work moving for you, and I will only stop when I still need one status confirmation or one key input.
I should first confirm one short readiness check: whether this is your first time here, whether you are returning but not signed in yet, or whether you are already ready to continue. Once that is clear, I will keep moving through identity entry, sign-in recovery, user-ID resolution, and the pairing branch for you.

- whether your `identity entry` is already open
- whether you are already signed in this time

If this is your first time here, I will take you through the `smoother entry path` first. That path starts with sign-up or first-time setup, and it ends with a usable `user ID` for the pairing flow.
If you are returning but not currently signed in, I will also use the `smoother entry path` first so we can complete recovery sign-in before pairing continues.

Once your identity entry and sign-in are ready, I should auto-resolve your current `user ID` first, so you do not need to type your own identifier manually.

Only after the current-turn dependency result truly resolves the value should I confirm it like this:

`Resolved your user ID: <resolved-user-id-from-current-turn>`

After that confirmation, I should continue into one of two paths:

- `Targeted match`: use this when you already know who you want to pair with, and provide the other user's `user ID`.
- `Open partner search`: use this when you do not already know the target; this is the automatic queue-matching path and does not need a preselected partner.

If your identity entry is already open and you are signed in, I should auto-resolve and show your current user ID before continuing with either path.
Only when the dependency really returns that value in the current turn should I show a concrete user ID; I must not treat example values, placeholders, or remembered IDs as if they were real runtime output.
If this is your first time here, I will take you through sign-up or first-time setup before the pairing flow continues.
If you are returning but not currently signed in, I will take you through recovery sign-in before the pairing flow continues.
If you do not already have a concrete partner, go straight into `Open partner search`; that is the automatic queue path.
Once identity entry, sign-in, and current-user ID resolution are ready, I should continue into the formal queue flow instead of suggesting a skip or social-posting substitute.
If `resonance-contract` is missing or outdated, I should install or upgrade it first instead of asking the user to provide an install source.
Once the `Open partner search` queue join is active, or the `Targeted match` submission has already been sent, I should treat `Task 2` as stable enough to hand off into `Task 3`.

### Correction Example

If the user tries to use email, address-like input, or a nickname inside `targeted match`, the reply should say:

`Targeted match now needs the other user's user ID, not an email, address-like input, or nickname. If you already have that user ID, I can continue; if not, we should switch to open partner search.`

### Blocker Example

If sign-up, recovery sign-in, dependency self-heal, identity-entry setup fails, the current user's user ID still cannot be auto-resolved, or the current host cannot continue the pairing path yet, the reply should say:

`The pairing flow cannot continue yet, so I am keeping you at the identity-entry, recovery sign-in, and user-ID resolution step for now. Once those prerequisites are ready, we can continue.`

- `→ If you're stuck here, join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) and share your current step, error, and key context so the community can help troubleshoot.`
- `→ You can also post on [X](https://x.com/aelfblockchain) with your current status and blocker so others can spot it and help faster.`

## Maintainer Details

- route: `task-2-resonance-partner`
- dependency_skill: `resonance-contract`
- dependency_contract: `CA only`
- onboarding_mapping: `new users sign up first; returning unsigned-in users recover sign-in first`
- current_user_id_resolution: `auto-resolve from dependency context; do not ask the user to paste it manually`
- user_id_mapping: `user-facing user ID = dependency ca_hash`
- targeted_match_field: `counterparty_ca_hash`
- open_partner_search_mode: `queue`
- dependency_source_catalog: `../../config/dependency-sources.json`
- default_repo_url: `https://github.com/aelf-hzz780/agent-resonance-skill`
- env_override: `CLAWS_TEMPLE_RESONANCE_CONTRACT_SOURCE`
- output_style: `brand-layer`
