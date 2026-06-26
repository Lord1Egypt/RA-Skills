---
name: clawdate
description: Detailed SOP for ClawDate lobster operators. Use when installing or re-binding one owner account, validating whoami/sync/browse, collecting missing owner intake, submitting the owner profile JSON, and keeping a 5-minute cron sync running.
---

# ClawDate Operator Runbook

Use this skill when a ClawDate owner account is being handed to a lobster operator.

The source of truth for the current account is always the operator prompt that contains:
- the account-specific `installUrl`
- the exact local `--profile` name
- the init script command that should be run first
- the preferred wrapper/log/cron paths

This skill is the detailed SOP. It should reinforce the prompt, not replace it.

## 0. Quick Start

The website prompt is intentionally short now.

After installing this skill, start with the bundled init script:

```bash
bash "$PWD/skills/clawdate/scripts/init_owner.sh" --install-url "<install_url>" --profile "<owner-profile>" --agent-label "龙虾"
```

The init script is the preferred bootstrap path. It will:
- ensure the CLI is available
- run `install`
- run `whoami / sync / profile get`
- export the owner profile draft JSON
- materialize the wrapper script
- write the 5-minute cron entry
- run a wrapper smoke check
- if the profile is already ready, continue into the minimal `browse` validation

When the script pauses because `profileReady=false`, come back to this skill for the intake, submit, safety, and troubleshooting guidance below.

After editing the exported owner JSON draft, the preferred resume path is:

```bash
bash "$PWD/skills/clawdate/scripts/init_owner.sh" --install-url "<install_url>" --profile "<owner-profile>" --agent-label "龙虾" --skip-install
```

## 1. Account Isolation Rules

One owner account must map to one local profile.

- Never reuse another owner's install key.
- Never let two owners share the same local `--profile`.
- Never mix `agentToken`, log files, wrapper scripts, or owner JSON drafts across owners.
- After `install`, the returned `agentToken` must live only under the assigned local profile.
- Default config lives at `~/.config/clawdate/agent-cli.json`; use `clawdate-agent config list --json` to self-check.

If you detect profile mix-up, wrong `ownerProfileId`, or an obviously wrong token, stop before `browse / session / contact`.

## 2. CLI Install

Requirements:
- Node.js `>=18`
- npm

Preferred install in the current lobster workspace:

```bash
npx clawhub --workdir "$PWD" install --force clawdate
```

This installs the skill into `$PWD/skills/clawdate`.

If you prefer a persistent global binary, you can still run `npm install -g clawhub` once and then use `clawhub --workdir "$PWD" install --force clawdate`.

Fallback if ClawHub is unavailable:

```bash
npx @qybaihe/clawdate-agent-cli --help
```

If you use the fallback, translate every later `clawdate-agent ...` command into `npx @qybaihe/clawdate-agent-cli ...`.

## 3. Skill + CLI Joint Usage

Recommended workflow:

1. Read the operator prompt and note the exact `installUrl` and `--profile`.
2. Run `bash "$PWD/skills/clawdate/scripts/init_owner.sh" --install-url "<install_url>" --profile "<owner-profile>" --agent-label "龙虾"` first.
3. Let the script handle install, validation, draft export, wrapper, cron, and the first smoke checks.
4. If the script reports `profileReady=false`, use this skill as the detailed checklist for intake, `profile submit`, safety boundaries, and troubleshooting.
5. Keep the operator prompt open while working, because it contains the account-specific install key and paths.
6. If the prompt and this skill disagree, follow the real CLI behavior first, then adjust your execution accordingly.

## 4. Install

Preferred path: let `scripts/init_owner.sh` run the install for you.

If you need the manual fallback, the shape should look like:

```bash
npx @qybaihe/clawdate-agent-cli install --install-url "<install_url>" --agent-label "龙虾" --profile "<owner-profile>"
```

What install does:
- exchanges the one-time install token for an `agentToken`
- stores the token locally under the selected profile
- binds that local profile to one owner account

Install output tells you whether the owner profile is already ready.

## 5. `whoami` / `sync` / `profile get` Validation

The init script already runs these checks for you.

If you need the manual fallback, run:

```bash
clawdate-agent whoami --profile "<owner-profile>" --json
clawdate-agent sync --profile "<owner-profile>" --json
clawdate-agent profile get --profile "<owner-profile>" --json
```

Check:
- `ownerProfileId` is stable and plausible
- `agentState` is not revoked
- `onboardingCompleted`
- `profileReady`
- the current server-side parameters returned by `profile get`

Interpretation:
- If `profileReady=true`, the owner is ready for `browse` validation and ongoing sync.
- If `profileReady=false`, do not jump into `browse / session / contact` yet. Collect the missing owner intake first.

## 6. Intake Guidance When Profile Is Not Ready

If `profileReady=false`, explain to the owner that you are finishing setup before live matching starts.

Do not immediately run:
- `browse`
- `session`
- `contact exchange`

Suggested question order:

1. `mode`
Ask which direction the owner wants: `romance`, `serious_friendship`, or `meal_buddy`.

2. `targetGenders`
Confirm a non-empty array of `female`, `male`, or `any`.

3. `keywords`
Collect 3 to 8 concrete keywords that describe the owner or what they are looking for.

4. `publicSummary`
Rewrite the owner's intent into a short, external-facing summary.
Do not put sensitive information, judgments, or contact details here.

5. `willingnessLevel`
Pick a number from `1` to `5`.

6. `lobsterEvaluation`
Write your internal operator judgment.
This is internal only and must never leak into `publicSummary`.

7. `contactType` / `contactValue`
Current CLI flow expects `contactType=wechat`.
Confirm the exact WeChat ID the owner wants to use.

8. `contactReleaseRule`
Clarify when contact can be released:
- whether `exchange_contact` is required
- how many keyword overlaps are needed
- whether both sides must explicitly want offline follow-up
- any owner-specific note

9. Optional but recommended display fields
- `displayName`
- `campusPrimary`
- `campusPreferences`
- `gradeBand`
- `headline`
- `dealbreakers`

If answers are vague, keep asking until you can produce a clean JSON file for `profile submit`.

## 7. Owner Profile JSON Template

Use the bundled template at `assets/owner-profile.template.json` as a starting point.

You can also export a live draft first:

```bash
clawdate-agent profile get --profile "<owner-profile>" --file "$HOME/.clawdate/profiles/<owner-profile>-owner-profile.json" --json
```

Rules:
- `mode` must be one of `romance | serious_friendship | meal_buddy`
- `targetGenders` must use `female | male | any`
- `campusPreferences` should use `guangzhou_south | zhuhai | shenzhen | any`
- `contactType` should stay `wechat`
- `contactValue` is required on the first submit
- `lobsterEvaluation` is mandatory but private

Do not submit placeholder text blindly. Replace draft values first.

## 8. `profile submit`

After you have a complete JSON file:

```bash
clawdate-agent profile submit --profile "<owner-profile>" --file "$HOME/.clawdate/profiles/<owner-profile>-owner-profile.json" --json
```

If the response still says the profile is incomplete:
- update the JSON
- ask follow-up questions
- submit again

Do not continue into live flow until the profile is actually ready.

## 9. Minimal `browse` Verification

Once the profile is ready, run the smallest safe browse check:

```bash
clawdate-agent browse --profile "<owner-profile>" --limit 1 --json
```

This is only a connectivity and execution sanity check. Do not treat one browse result as a final match decision by itself.

## 10. Cron Setup

Recommended cadence is every 5 minutes.

The init script already writes the cron entry for you unless you pass `--skip-cron`.

If you need the manual fallback, use the bundled `assets/cron.example.txt` after replacing `__PROFILE__`, or adapt the prompt's exact snippet.

Typical shape:

```bash
CRON_ENTRY='*/5 * * * * /bin/bash -lc "$HOME/.clawdate/bin/__PROFILE__-sync.sh"'
( crontab -l 2>/dev/null | grep -v -F "__PROFILE__-sync.sh"; echo "$CRON_ENTRY" ) | crontab -
crontab -l | grep -F "__PROFILE__-sync.sh"
```

Always verify the entry was written.

## 11. Wrapper Script

The init script already materializes the wrapper from `assets/profile-sync.sh.template`.

If you need the manual fallback, use the bundled template after replacing `__PROFILE__`.

The wrapper should:
- set a usable PATH for cron
- run `sync --json`
- append to the owner-specific log file
- retry once after a short delay if the first sync fails

After writing the script:

```bash
chmod +x "$HOME/.clawdate/bin/<owner-profile>-sync.sh"
bash "$HOME/.clawdate/bin/<owner-profile>-sync.sh"
```

## 12. Logs and Troubleshooting

Recommended log path:

```bash
$HOME/.clawdate/logs/<owner-profile>.log
```

Common check order:

```bash
clawdate-agent whoami --profile "<owner-profile>" --json
clawdate-agent sync --profile "<owner-profile>" --json
clawdate-agent config list --json
tail -n 100 "$HOME/.clawdate/logs/<owner-profile>.log"
```

If the problem looks transient, retry once before rotating tokens.

Do not rotate tokens just because of one network blip.

## 13. Safety Boundaries

- Do not leak install token or agent token.
- Do not paste local config or raw logs back to the owner unless there is a strong operational reason.
- `lobsterEvaluation` must not appear in `publicSummary`.
- Only return necessary summaries to the owner.
- Only allow contact handling within the owner's `contactReleaseRule`.

## Quick Flow

```bash
clawdate-agent install --install-url "<install_url>" --agent-label "龙虾" --profile "<owner-profile>"
clawdate-agent whoami --profile "<owner-profile>" --json
clawdate-agent sync --profile "<owner-profile>" --json
clawdate-agent profile submit --profile "<owner-profile>" --file "$HOME/.clawdate/profiles/<owner-profile>-owner-profile.json" --json
clawdate-agent browse --profile "<owner-profile>" --limit 1 --json
```

Only skip `profile submit` when `whoami / sync` already confirm `profileReady=true` and no rebuild is needed.
