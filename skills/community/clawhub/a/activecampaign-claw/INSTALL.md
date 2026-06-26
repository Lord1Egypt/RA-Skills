# Installing the ActiveCampaign Skill

This skill has a one-time **calibration** step that scans your account so the agent operates on real data instead of generic advice. Calibration requires API credentials.

## Prerequisites

- ActiveCampaign account (Plus tier or higher recommended for full feature access)
- `python3` (3.10+) installed and on PATH
- OpenClaw workspace where the skill will be installed

## Step 1: Get your API credentials from ActiveCampaign

1. Log in to your ActiveCampaign account
2. Click the **gear icon** (bottom-left corner) → **Settings**
3. Click **Developer** in the left sidebar
4. You'll see two values on that page:
   - **URL** — looks like `https://yourcompany.api-us1.com`
   - **Key** — a long string of letters and numbers

Keep this page open — you'll need both values in Step 3.

> **Tip:** The URL on the Developer page is your **API URL** (`yourco.api-us1.com`), which is different from your login URL (`yourco.activehosted.com`). Use the API URL — calibration will fail with a 404 against the login URL.

> **Use a dedicated, least-privileged integration user.** AC tokens are scoped to the user that created them. If that user is deleted or deactivated, every integration using their token breaks. Create a service-account user (`integration-bot@yourco.com`) and grant it only the permissions you actually need — typically Contacts and Deals access, plus whichever lists/automations the workflows you intend to use will touch. Admin is **not** required and not recommended. Generate the token from **that** user's Developer page and use it here.

## Step 2: Install the skill

```bash
openclaw skills install ji282h7/activecampaign-claw
```

Verify it landed:

```bash
openclaw skills list | grep activecampaign
ls ~/.openclaw/skills/activecampaign/SKILL.md
```

If the skill doesn't appear in `openclaw skills list`, the install didn't register. Re-run with `--verbose` for diagnostics.

## Step 3: Set credentials

The skill reads `AC_API_URL` and `AC_API_TOKEN`. It checks environment variables first, then the OS keychain (if `keyring` is installed). Pick the option that matches how you run things.

### Option A — OpenClaw config (recommended)

This makes credentials available to every agent the OpenClaw gateway launches. After setting, restart the gateway so agents pick up the new env.

```bash
openclaw config set env.vars.AC_API_URL "https://YOURACCOUNT.api-us1.com"
openclaw config set env.vars.AC_API_TOKEN "YOUR-TOKEN-HERE"
openclaw gateway restart
```

Replace `YOURACCOUNT` with your subdomain. Use the API URL exactly as shown on the Developer page — no trailing slash, no `/api/3` suffix (the client appends that itself).

Verify:

```bash
openclaw config get env.vars.AC_API_URL
```

### Option B — Shell profile (for direct script runs)

If you'll run the calibration / audit scripts directly from your terminal (outside an OpenClaw agent), export the vars from your shell rc file.

Add to `~/.zshrc` (or `~/.bashrc` if you use bash):

```bash
export AC_API_URL="https://YOURACCOUNT.api-us1.com"
export AC_API_TOKEN="YOUR-TOKEN-HERE"
```

Reload your shell:

```bash
source ~/.zshrc   # or: source ~/.bashrc
```

### Option C — OS keychain (optional)

If you'd rather not have the token in plaintext on disk, install the `keyring` package and store credentials in your OS keychain (macOS Keychain, Windows Credential Manager, or libsecret on Linux).

```bash
pip install keyring
python3 scripts/auth.py set "https://YOURACCOUNT.api-us1.com" "YOUR-TOKEN-HERE"
```

Verify with:

```bash
python3 scripts/auth.py status
```

The skill checks env vars first, then the keychain. If you set both, env vars win — handy for testing against a sandbox without disturbing your production token.

Verify:

```bash
echo "$AC_API_URL"
[ -n "$AC_API_TOKEN" ] && echo "token set" || echo "token MISSING"
```

> **You can use both A and B.** Setting them in OpenClaw config covers gateway-launched agents; exporting them in your shell covers direct CLI runs. The values should match.

## Step 4: Validate and calibrate

```bash
# Cheapest live call — confirms auth, exits
python3 ~/.openclaw/skills/activecampaign/scripts/calibrate.py --validate

# Full calibration (30–90s) — scans lists, tags, custom fields, pipelines,
# automations, and 90 days of campaign performance
python3 ~/.openclaw/skills/activecampaign/scripts/calibrate.py

# Or taxonomy-only (faster, skips baseline computation) for a quick smoke test
python3 ~/.openclaw/skills/activecampaign/scripts/calibrate.py --quick
```

Calibration writes `~/.activecampaign-skill/state.json`. Nothing is sent back to AC.

## Step 5: Verify the skill works

Start a new OpenClaw session and ask:

```
"Run a list health audit on my AC account"
```

The agent should read `state.json`, load the recipe, execute the audit script, and summarize results.

## Step 6: Schedule monthly recalibration (optional)

Create a wrapper that sources your credentials, then add a cron entry pointing at it:

```bash
# ~/.activecampaign-skill/recalibrate.sh
#!/bin/bash
source ~/.zshrc   # or ~/.bashrc — wherever AC_API_URL and AC_API_TOKEN are exported
python3 ~/.openclaw/skills/activecampaign/scripts/calibrate.py
```

```bash
chmod 700 ~/.activecampaign-skill/recalibrate.sh
crontab -e

# Runs at 9am on the 1st of each month
0 9 1 * * ~/.activecampaign-skill/recalibrate.sh >> ~/.activecampaign-skill/calibrate.log 2>&1
```

> **Do not put your API token directly in the crontab.** Crontab entries are readable by the user's account and may appear in logs. Use the wrapper-script pattern above so credentials stay in your shell profile.

## Troubleshooting

**`401 Unauthorized` during calibration:**
- Check the token is set: `echo $AC_API_TOKEN` (or `openclaw config get env.vars.AC_API_TOKEN`)
- Check the user that created the token is still active in AC
- Regenerate the token in AC's Developer settings

**`404 Not Found` during calibration:**
- You probably used the login URL (`yourco.activehosted.com`) instead of the API URL (`yourco.api-us1.com`). Update and re-run.
- Don't include `/api/3` in the URL — the client appends it.

**`429 Too Many Requests` during calibration:**
- Another integration is consuming your rate limit. Wait 60 seconds and retry.

**Calibration succeeds but state.json is sparse:**
- Your account may not have 90 days of campaigns yet. Defaults are used.

**Agent doesn't seem account-aware:**
- Check the calibration timestamp: `cat ~/.activecampaign-skill/state.json | jq '.last_calibrated'`
- If >30 days old, recalibrate.
- If you set credentials via OpenClaw config and didn't restart the gateway, agents won't see them yet — `openclaw gateway restart`.

## Uninstalling

```bash
openclaw skills uninstall activecampaign
rm -rf ~/.activecampaign-skill   # removes state and history
```

State and history files are NOT removed automatically on uninstall. If you reinstall, your data is preserved.

To also remove credentials:

```bash
openclaw config unset env.vars.AC_API_URL
openclaw config unset env.vars.AC_API_TOKEN
```

And/or remove the `export` lines from `~/.zshrc` / `~/.bashrc`.

## Privacy

All data stays local:
- `~/.activecampaign-skill/state.json` — account taxonomy and baselines
- `~/.activecampaign-skill/history.jsonl` — record of recipes run

Nothing is sent anywhere except your own AC account via your own token. No third-party gateways, no telemetry.
