# Bumble Client

OpenClaw skill for driving Bumble through a Remote Browser Service (RBS).

## What It Does

- Restores or creates a Bumble session
- Runs the phone-number auth flow
- Accepts SMS verification codes
- Lists matches and reads messages
- Sends messages
- Extracts profile details and exports profile photos

## Requirements

- Python 3
- `requests`
- Access to the Remote Browser Service
- `AC_API_KEY` when the RBS endpoint requires authentication

Optional environment variables:

- `AC_API_KEY`: bearer token for RBS requests
- `RBS_BASE_URL`: override the default RBS base URL

Install dependency:

```bash
python3 -m pip install requests
```

## How To Use

Run commands from this skill directory.

Inspect state:

```bash
python3 scripts/bumble_client.py state
python3 scripts/bumble_client.py debug
python3 scripts/bumble_client.py content
python3 scripts/bumble_client.py snapshot
```

Start auth flow:

```bash
python3 scripts/bumble_client.py auth "<user_phone_number>"
```

Submit SMS code:

```bash
python3 scripts/bumble_client.py sms_code "<6-digit-code>"
```

List matches:

```bash
python3 scripts/bumble_client.py matches
```

Read messages:

```bash
python3 scripts/bumble_client.py messages "Kritika"
```

Send a message:

```bash
python3 scripts/bumble_client.py send "Kritika" "Hello there"
```

Fetch a profile:

```bash
python3 scripts/bumble_client.py profile "Kritika"
```

Export photos:

```bash
python3 scripts/bumble_client.py photos "Anya" "/absolute/output/dir"
```

## Notes

- The phone number must be provided by the user at runtime.
- The skill reuses the stored `bumble` session when possible.
- The skill sets location to San Francisco after session start.
- CAPTCHA and passkey-related screens may still require manual intervention.
- Bumble UI changes can break selectors or parsing logic.
