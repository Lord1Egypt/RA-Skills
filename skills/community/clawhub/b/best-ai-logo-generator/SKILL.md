---
name: ai-logo-generator
version: 1.0.0
description: "Generate professional AI logos using ailogogenerator.online. Use this skill whenever the user wants to create a logo, brand icon, app icon, favicon, or any visual identity asset — even if they don't explicitly mention 'logo generator'. Covers requests like 'make me a logo', 'design an icon for my app', 'I need a brand mark', or 'generate a logo for my startup'."
license: MIT-0
---

# AI Logo Generator Skill

You are now equipped to generate professional logos via the ailogogenerator.online API. Use this skill for any logo, icon, or brand identity generation request.

## Why follow this flow

The API is stateful — generation is async and requires polling. Skipping the poll loop means you'll never get the image URL. Auth tokens are long-lived but can expire; always check before generating so the user doesn't hit a mid-session 401. Always download the image locally so the user actually has the file, not just a URL.

## Step 1: Authentication

Read `~/.config/ailogogenerator.online/auth.json`.

If the file exists and has a non-empty `token` field, you're authenticated. Use that token as the Bearer token for all API calls.

If the file doesn't exist or the token is missing/empty, run the login script:

```bash
node <SKILL_DIRECTORY>/login.mjs
```

Replace `<SKILL_DIRECTORY>` with the actual directory where this `skill.md` lives. You can find it by checking `$CLAUDE_SKILL_DIR` or resolving the path relative to this file.

After the script exits, re-read auth.json to get the token. If it's still missing, tell the user the login failed and ask them to try again.

## Step 2: Gather requirements

Ask the user for the following. Subject is required; all others are optional with sensible defaults.

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `subject` | string | Yes | What the logo represents — "a coffee shop", "a fintech startup", "a dog grooming brand" |
| `vibe` | string | No | Style/mood — "modern", "playful", "minimalist", "bold", "elegant", "techy", "vintage" |
| `colors` | string[] | No | Hex color array — `["#1a1a2e", "#e94560"]`. Empty array = AI chooses |
| `text` | string or null | No | Text to render in the logo. Pass `null` for icon-only (no text) |
| `withBackground` | boolean | No | Whether to include a background (default `false` = transparent) |
| `shape` | string | No | Logo shape — "square", "circle", "hexagon", "free" |
| `detail` | string | No | Additional free-text detail — "use a coffee cup silhouette", "include a lightning bolt" |

If the user gave you enough info in their initial message, proceed directly. Don't make them answer questions they already answered. If key info is missing, ask once — cover all gaps in a single question.

## Step 3: Generate the logo

Call the generate endpoint:

```
POST https://ailogogenerator.online/api/ai/logo/generate
Content-Type: application/json
Authorization: Bearer <token>

{
  "params": {
    "subject": "...",
    "vibe": "...",
    "colors": ["#hex1", "#hex2"],
    "text": "BrandName" or null,
    "withBackground": false,
    "shape": "square",
    "detail": "..."
  }
}
```

Successful response:
```json
{
  "success": true,
  "data": {
    "taskId": "task_abc123",
    "params": { ... }
  }
}
```

Note: Each generation costs 4 credits. New accounts receive bonus credits on registration.

## Step 4: Poll for completion

Call the query endpoint every 3 seconds until status is `"completed"`:

```
POST https://ailogogenerator.online/api/ai/logo/query
Content-Type: application/json
Authorization: Bearer <token>

{
  "taskId": "task_abc123"
}
```

Response while processing:
```json
{ "success": true, "data": { "status": "processing" } }
```

Response when done:
```json
{
  "success": true,
  "data": {
    "status": "completed",
    "imageUrl": "https://cdn.ailogogenerator.online/logos/abc123.png"
  }
}
```

Poll up to 60 times (3 minutes total). If it's still not done after that, tell the user the generation timed out and they can check the website.

Show the user a progress indicator while polling — something like "Generating... (10s elapsed)" updated every few seconds.

## Step 5: Download the image

Download the image from `imageUrl` to the current working directory. Use a descriptive filename based on the subject, e.g., `logo-coffee-shop.png`. If a file with that name already exists, add a timestamp suffix.

Announce the saved path to the user.

## Error handling

Handle these cases gracefully — don't show raw HTTP errors to the user:

- **401 Unauthorized**: Token expired. Delete `~/.config/ailogogenerator.online/auth.json`, then re-run `login.mjs` to get a fresh token. Then retry the generation automatically.

- **402 Payment Required**: Insufficient credits. Tell the user: "You're out of credits. Visit https://ailogogenerator.online to top up and come back."

- **429 Too Many Requests**: Daily limit reached. Tell the user: "You've hit the daily limit. Log in at https://ailogogenerator.online to get more credits or wait until tomorrow."

- **Network error**: Retry once after 2 seconds. If it fails again, report the error and suggest checking their internet connection.

- **Generation failed** (status = "failed" in query response): Tell the user generation failed and offer to try again with adjusted parameters.

## Example interaction

```
User: make me a logo for my SaaS called "Stackly" — dark techy vibe, purple and black

You: Generating your logo for Stackly...
     [calls generate API with subject="SaaS product", vibe="techy", colors=["#6d28d9","#0f0f0f"], text="Stackly"]
     Generating... (6s elapsed)
     Generating... (9s elapsed)
     Done! Saved to ./logo-stackly.png
```

## Important notes

- Never show the raw API token to the user
- If the user wants multiple variations, run the generate+poll cycle multiple times, saving each with a variant suffix
- The API is HTTPS only; never downgrade to HTTP
- After a successful 401 re-auth, retry the original request exactly once — if it fails again, stop and ask the user to re-login manually
