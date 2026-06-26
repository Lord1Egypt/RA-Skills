---
name: findmy-icloud-cli
description: Query Apple Find My device and family-device locations through the pyicloud iCloud CLI, using a locally stored Apple ID username in a deterministic state file instead of hardcoding it. Use when the user wants current locations, battery status, or device lookups for their own Apple devices or family-shared devices, and when a reliable CLI path is preferred over flaky Find My UI automation.
---

# Find My iCloud CLI

Use this skill for Apple Find My lookups via the `icloud` CLI (`pyicloud` 2.5.0+).
This is the reliable path for device and family-device location on this Mac.

Run scripts from:

```bash
cd /Users/rolandk/.openclaw/workspace/skills/findmy-icloud-cli
```

## State and setup

Do not hardcode the user's Apple ID in the skill.
Store it once in this deterministic state file:

```text
~/.local/state/icloud-findmy-cli/account.env
```

Format:

```bash
ICLOUD_FINDMY_USERNAME="their.email@example.com"
```

Use:

```bash
./scripts/findmy.sh set-username their.email@example.com
./scripts/findmy.sh show-username
```

If the username is missing, stop and ask the user once for their Apple ID email. After that, persist it via `findmy.sh set-username` and reuse the state file.

## Auth flow

Check current auth:

```bash
./scripts/findmy.sh auth-status
```

If not logged in:

```bash
./scripts/findmy.sh auth-login
```

That opens the current `pyicloud` auth flow using the stored username. The user may need to enter password and 2FA.

## Core commands

### Resolve a person to the best device automatically

When the user asks for a person's location in natural language, do not force them to name a device.
Use `scripts/person-find.py` first.

Do not hardcode real family names into the skill. Store person aliases in a local state file instead:

```text
~/.local/state/icloud-findmy-cli/people-aliases.json
```

Set aliases with neutral labels such as `me`, `partner`, `kid`, or any user-chosen nickname:

```bash
./scripts/findmy.sh set-person-alias me "Roland"
./scripts/findmy.sh set-person-alias partner "Gabriella"
./scripts/findmy.sh show-person-aliases
```

Default resolution order:
1. Match the person's iPhone
2. If no matching iPhone with location is available, match their Apple Watch
3. If neither is available, fall back to another matching device
4. If nothing matches, say so clearly

Examples:

```bash
./scripts/person-find.py "partner"
./scripts/person-find.py "me"
./scripts/person-find.py "kid"
```

### List all devices with live location

```bash
./scripts/findmy.sh list
```

This runs:

```bash
icloud devices list --username "$USERNAME" --with-family --locate --format json
```

### Show one device in detail

```bash
./scripts/findmy.sh show "Roland’s iPhone 14 Pro"
```

### Find devices by fuzzy name match

```bash
./scripts/device-find.py "Gabriella"
./scripts/device-find.py "iPhone 14"
```

## Output shape

The main command returns JSON list entries with fields like:
- `id`
- `name`
- `display_name`
- `device_class`
- `device_model`
- `battery_level`
- `battery_status`
- `location.latitude`
- `location.longitude`
- `location.timeStamp`
- `location.horizontalAccuracy`

Prefer JSON parsing over text scraping.

## Working rules

- Use this skill for Apple devices and family-shared devices, not shared-person Find My contacts.
- If the user asks for a person like "where is my partner?", use `scripts/person-find.py` instead of asking for a device name.
- Prefer user-defined aliases from `people-aliases.json`, not hardcoded real names in the skill.
- Prefer iPhone first, then Apple Watch, then other matching devices.
- Prefer `findmy.sh list` first when broad inspection is needed.
- Use `findmy.sh show` when the exact device name is already known.
- If auth breaks after an upgrade, re-check with `icloud --help`, then re-run `findmy.sh auth-login`.
- Do not ask for the Apple ID again if the state file already has it.
- Do not store passwords in the state file.

## Limits

- This skill does not track shared people from the Find My People tab.
- Some accessories may return `location: null` or stale data.
- Family device visibility depends on Find My / Family Sharing state.

## Scripts

- `scripts/findmy.sh` is the main wrapper for username storage, auth, device list, and device show
- `scripts/state.sh` handles deterministic local state storage
- `scripts/device-find.py` filters devices by case-insensitive substring match
- `scripts/person-find.py` resolves a person alias/name to the best matching device, preferring iPhone then Watch
