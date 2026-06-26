---
name: ebusy-courts
description: Query eBusy-based tennis hall bookings via a small Python client.
homepage: https://clawhub.com
metadata:
  openclaw:
    emoji: 🎾
    requires:
      bins: ["python"]
      env: []
---

# eBusy Courts Skill

This skill wraps a small Python client (`ebusy_api.py`) to log into
**eBusy**-based booking systems and fetch reservations for a given
court-module and date.

It is designed to work with **multiple halls** by switching
configuration via environment variables. All hall- and user-specific
values are provided by the environment, not hard-coded in the skill.

> **Important:** No usernames/passwords should be committed into this
> skill folder. Keep real credentials in a local `.env`, your shell
> environment, or OpenClaw's gateway config.

---

## Files

- `skills/ebusy-courts/ebusy_api.py` – core Python client
- `skills/ebusy-courts/SKILL.md` – this documentation

Optional (local-only, **do not publish**):

- `skills/.env` – local environment file with hall-specific credentials

---

## Python client: ebusy_api.py

The client is written to be **generic**; it reads all hall-specific
config from environment variables:

```bash
EBUSY_BASE_URL       # e.g. https://myclub.ebusy.de
EBUSY_USERNAME       # login user for the chosen hall
EBUSY_PASSWORD       # login password for the chosen hall
EBUSY_COURT_ID       # eBusy court-module id for this hall
EBUSY_FIRST_COURT_NO # first court number inside that module
```

Usage (in a venv with `requests` + `beautifulsoup4` installed):

```bash
source venv/bin/activate
export EBUSY_BASE_URL="https://myclub.ebusy.de"
export EBUSY_USERNAME="<your-user>"
export EBUSY_PASSWORD="<your-password>"
export EBUSY_COURT_ID="<module-id>"
export EBUSY_FIRST_COURT_NO="<first-court-no>"

python skills/ebusy-courts/ebusy_api.py 03/07/2026
```

The script will:

1. Log into the configured eBusy instance using the configured
   username/password.
2. Fetch the reservations JSON for the given date.
3. Print a sorted list of reservations:

   ```text
   Reservierung Platz 1: 09:00 - 10:00 von <Text>
   Reservierung Platz 2: 10:00 - 11:00 von <Text>
   ...
   ```

---

## Example hall profiles

This section shows **example configurations** for two real halls in
Germany. Other users can copy the pattern and plug in their own club
URLs and module IDs.

### Example: Medenhalle Wiesbaden-Medenbach

- Base URL: `https://medenhalle.ebusy.de`
- `EBUSY_COURT_ID = 1`
- `EBUSY_FIRST_COURT_NO = 1`
- Credentials typically provided via:
  - `MEDENHALLE_USER`
  - `MEDENHALLE_PASSWORD`

Example shell setup:

```bash
source venv/bin/activate
# load your local secrets, e.g. from skills/.env
export EBUSY_BASE_URL="https://medenhalle.ebusy.de"
export EBUSY_USERNAME="$MEDENHALLE_USER"
export EBUSY_PASSWORD="$MEDENHALLE_PASSWORD"
export EBUSY_COURT_ID="1"
export EBUSY_FIRST_COURT_NO="1"

python skills/ebusy-courts/ebusy_api.py 03/07/2026
```

### Example: KTEV Kelkheim

- Base URL: `https://ktev.ebusy.de`
- `EBUSY_COURT_ID = 807`
- `EBUSY_FIRST_COURT_NO = 2135`
- Credentials typically provided via:
  - `KTEV_USER`
  - `KTEV_PASSWORD`

Example shell setup:

```bash
source venv/bin/activate
# load your local secrets, e.g. from skills/.env
export EBUSY_BASE_URL="https://ktev.ebusy.de"
export EBUSY_USERNAME="$KTEV_USER"
export EBUSY_PASSWORD="$KTEV_PASSWORD"
export EBUSY_COURT_ID="807"
export EBUSY_FIRST_COURT_NO="2135"

python skills/ebusy-courts/ebusy_api.py 03/07/2026
```

---

## How an agent can use this skill

When a user asks for availability in a given hall (e.g. "Suche freie
Zeiten in der Tennishalle XYZ am Sonntag"), an OpenClaw agent can:

1. Map the hall name to a profile (base URL, module id, first-court-no),
   either from `TOOLS.md` or agent-specific config.
2. Ensure the environment variables `EBUSY_*` are set for that hall
   (credentials supplied by the runtime or `skills/.env`).
3. Call `ebusy_api.py` for the relevant date, parse the JSON, and build
   an availability table (free vs booked) per court and time slot.

The **decision logic** (which profile to choose for which user request)
should live in the agent and/or `TOOLS.md`, not in this skill's code.

---

## Publishing considerations

- Do **not** publish `skills/.env` or any file containing real
  credentials to ClawHub.
- Ensure `.gitignore` excludes `skills/.env` and similar secret-bearing
  files.
- The skill itself (this `SKILL.md` + `ebusy_api.py`) contains only
  generic logic and non-secret configuration; the example profiles are
  illustrative and can be replaced by any other eBusy-based club.
