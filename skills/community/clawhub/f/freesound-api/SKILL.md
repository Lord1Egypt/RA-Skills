---
name: freesound-api
description: Set up and use Freesound API access from a local Windows OpenClaw workspace with OAuth login, local credential storage, and sound search helpers. Use when the user wants to register or use a Freesound API app, save a Freesound client id and client secret locally, complete localhost OAuth login, search Freesound sounds, or fetch Freesound data without exposing secrets in a published skill.
---

# freesound-api

Use this as a local-only skill. Do not publish Freesound client secrets inside the skill.

## Local storage

This skill stores credentials in:

- `%APPDATA%\OpenClaw\freesound-api\credentials.json`

Keep the secret there, not in `SKILL.md`.

## Setup credentials

Save the app credentials locally:

```powershell
python scripts\setup_credentials.py --client-id '<CLIENT_ID>' --client-secret '<CLIENT_SECRET>' --redirect-uri 'http://localhost:8787/callback'
```

Use the same redirect URI here that was registered in Freesound.

## Complete OAuth login

Run:

```powershell
python scripts\oauth_login.py
```

What it does:

1. Starts a temporary localhost callback server on port `8787`
2. Opens the Freesound authorization page in the browser
3. Receives the authorization code at `http://localhost:8787/callback`
4. Exchanges it for an access token
5. Saves the token back into `%APPDATA%\OpenClaw\freesound-api\credentials.json`

If the browser does not open, copy the printed URL manually.

## Search sounds

Run:

```powershell
python scripts\search_sounds.py "rain" --page-size 10
```

Examples with filters:

```powershell
python scripts\search_sounds.py "rain" --license cc0 --duration-min 5 --duration-max 60
python scripts\search_sounds.py "thunder" --tag storm --tag ambience
python scripts\search_sounds.py "wind" --filter "samplerate:[44100 TO *]"
```

The search helper prefers OAuth bearer token auth if available. If there is no OAuth token yet, it falls back to using the saved Freesound secret as the `token` parameter for simple API calls.

## Get sound details

Run:

```powershell
python scripts\sound_details.py 322965
```

Use this to inspect metadata, previews, ratings, tags, format details, and the direct download endpoint for a sound.

## Download a sound

Run:

```powershell
python scripts\download_sound.py 322965 --out-dir downloads
```

Download a preview instead of the original file:

```powershell
python scripts\download_sound.py 322965 --preview hq-mp3 --out-dir previews
```

This saves the original file or selected preview into the chosen output directory using the current OAuth token or saved API key.

## Public-safe publishing

If publishing this skill publicly, publish only the skill folder and scripts. Do not publish `%APPDATA%\OpenClaw\freesound-api\credentials.json` or any client secret.

## Notes

- Keep the redirect URI consistent. A mismatch will break the token exchange.
- Prefer OAuth login for user-level access.
- If a secret was pasted into chat, treat it as exposed and rotate it after testing.
- If `requests` is missing locally, install it in the Python environment before running the scripts.
