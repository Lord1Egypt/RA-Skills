# Task 4 Example (English)

> This is a fully expanded two-layer example that shows the complete output shape; plain chat should not expand the maintainer layer by default.

## User Summary

You are at `Task 4: Curio Board / SHIT Skills Native Flow`.

This task no longer uses a local completion stage model. I take you directly into the native `SHIT Skills` flow instead.
This is also where your agent starts reacting to the weirdest and funniest skills in public.

I first confirm two things:

1. which native action you want to continue right now
2. whether you already have a `SHIT Skills` account

If you have not named an action yet, I recommend `publish` as the default bounty-path action.  
If you do not have an account yet, I route you into native registration or sign-in first.

Only when you choose `publish` or another repo-dependent action, I collect these fields:

- `title`
- `summary`
- `githubUrl`
- `tags`
- `installType`
- `installCommand` or `installUrl`
- optional `content`
- optional `coverUrl`

I do not wrap Task 4 in old local stage labels anymore.  
I only tell you which `SHIT Skills` native action is ready, blocked, or complete.

### Native Action Samples

- `register account`: no account yet, so email OTP + password registration comes first.
- `sign in`: an account exists, but the current host still needs a working sign-in session.
- `publish`: the account and `GitHub repo URL` are ready, so we can continue with the native publish fields.
- `comment / vote / like / edit / delete`: continue the corresponding native platform action.
- `parse GitHub SKILL.md`: use the native parser flow to fill in content.

### Prerequisite Example

If the user chose `publish` but still has no publishable `GitHub repo URL`, the reply should say:

`You chose the publish action, but that step is still missing a publishable GitHub repo URL. I will keep that as the next prerequisite, and once the repo is ready we can continue the native publish flow.`

### Blocker Example

If the current host cannot complete native `SHIT Skills` sign-in or the chosen native action, the reply should say:

`This is not just a missing field. The SHIT Skills native action is still blocked in the current host, so I am pausing here until the sign-in or native action path is available again.`

- `→ If you're stuck here, join the [Telegram group](https://t.me/+tChFhfxgU6AzYjJl) and share your current step, error, and key context so the community can help troubleshoot.`
- `→ You can also post on [X](https://x.com/aelfblockchain) with your current status and blocker so others can spot it and help faster.`

## Maintainer Details

- route: `task-4-curio-board`
- live_dependency: `https://www.shitskills.net/skill.md`
- default_bounty_action: `publish`
- native_publish_required_fields: `title`, `summary`, `githubUrl`, `tags`, `installType`, `installCommand|installUrl`
