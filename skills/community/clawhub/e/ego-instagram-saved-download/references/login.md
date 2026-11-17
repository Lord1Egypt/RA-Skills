# Sign in to Instagram once in Ego Lite

This skill reads **your** Saved posts with cookies already in Ego Lite. It checks login itself. There is no separate cookie-healthcheck skill. It never types a password or prints cookie values.

Every JSON result includes `login_tip` and `login_tip_zh`. The agent must show that text: signing in inside Ego Lite is what makes Saved readable. Anonymous mode cannot see the archive.

## When the script soft-fails

`login_required: true`, exit code `2`, and `how_to_login` / `how_to_login_zh`. No media is saved.

Signals (booleans only):

- Logged out: a password field, a username field, or an `/accounts/login` URL.
- Logged in: no password field, and an inbox link or a `ds_user_id` cookie name visible to the page. A Saved link by itself is not enough.

## Do this once

1. Open **Ego Lite**. `ego-browser` drives that profile.
2. Visit https://www.instagram.com/accounts/login/ and sign in yourself.
3. Leave the profile logged in and re-run:

```bash
node skills/instagram-saved-download/scripts/download.mjs \
  --count 5 --out /tmp/ig-saved
```

`--keep` leaves the tab open so you can sign in there, then run again.

## Optional Chrome import

```bash
ego-browser import list
ego-browser import --browser chrome --profile Default
```

Confirm Instagram shows your Saved page in the Ego window. Do not paste cookies into issues or this repo.
