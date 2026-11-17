# Sign in to Pinterest once in Ego Lite

This skill reuses cookies already stored in Ego Lite. It never types a password or prints cookie values.

Every JSON result includes `login_tip` and `login_tip_zh`. The agent must show that text to the user: **signing in inside Ego Lite improves results** (real numeric pin ids, related pins, boards). Anonymous mode (`--allow-anonymous`) still returns public images, but ids are often `e1_…` and related or board calls are weaker.

## When the script soft-fails

`login_required: true`, exit code `2`, and `how_to_login` / `how_to_login_zh`. No images are saved. `manifest.json` repeats the same instructions.

Signals (booleans only):

- Logged out: `[data-test-id="unauth-header"]` or `[data-test-id="simple-login-button"]`, or a `/login` / `/signup` URL.
- Logged in: a profile control, or `_auth=1` visible to the page, and no logged-out header.

## Do this once

1. Open the **Ego Lite** app. `ego-browser` drives that profile.
2. Visit https://www.pinterest.com/login/ yourself and sign in.
3. Leave the profile logged in and re-run without `--allow-anonymous`.

```bash
node skills/pinterest-download/scripts/download.mjs \
  --query wallpaper --count 2 --out /tmp/ego-pinterest-wallpaper
```

`--keep` leaves the tab open so you can sign in there, then run again.

## Optional Chrome import

```bash
ego-browser import list
ego-browser import --browser chrome --profile Default
```

Confirm in the Ego window that pinterest.com shows your avatar. Do not paste cookies into issues or this repo.
