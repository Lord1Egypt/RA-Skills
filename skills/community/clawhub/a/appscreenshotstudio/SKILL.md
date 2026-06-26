---
name: appscreenshotstudio
description: Generate production-ready App Store and Play Store screenshots from your codebase. Reads your app's colors, screens, and copy — then creates a finished screenshot set in exact store dimensions.
homepage: https://appscreenshotstudio.com/openclaw
metadata: {"clawdbot":{"emoji":"📱","env":["APPSCREENSHOTSTUDIO_API_KEY"],"tags":["ios","android","app-store","screenshots","aso","marketing"]}}
---

Generate finished App Store / Play Store screenshots directly from your terminal.

## Setup

Requires `APPSCREENSHOTSTUDIO_API_KEY` in your environment. Get a key at https://appscreenshotstudio.com/settings (requires an account with credits).

## When to use this skill

Use when the user says: "generate screenshots", "App Store screenshots", "Play Store screenshots", "store listing", "marketing screenshots", or wants to ship a new app.

## Workflow

### Step 1 — Research the codebase

Before calling the API, gather context from the project. This context directly improves the generated layouts, colors, and headlines.

Find and read:
- `README.md` — app name, purpose, main features
- `package.json` / `pubspec.yaml` / `Cargo.toml` / `build.gradle` — app name, tech stack
- Brand colors: `tailwind.config.*` (`theme.extend.colors`), SwiftUI `Color(`, Flutter `ThemeData`
- Key screens: Next.js `app/` routes, SwiftUI `NavigationView`/`TabView`, Flutter `GoRouter`
- App Store metadata: `Info.plist`, fastlane `metadata/`, `AndroidManifest.xml`

Build this context:
```
app_name, readme_summary, key_screens[], color_tokens{}, target_audience,
app_category (fitness|finance|social|productivity|food|travel|health|education|other),
competitive_edge, ui_style, primary_user_flow
```

### Step 2 — Confirm with the user

Show what you found and ask:
- "I found these main features: [X, Y, Z]. Which 3-5 should I highlight?"
- "Your brand color appears to be [#hex]. Should I use it?"
- "Mood? Options: minimal, bold, playful, professional, dark, warm, energetic"
- "Device? iphone-6.9 (default), ipad-13, android-phone, android-tablet-10"
- "How many screenshots? (3–8, default 5)"

### Step 3 — Create project and generate

**3a. Create a project:**

```bash
curl -s -X POST https://appscreenshotstudio.com/api/v1/projects \
  -H "Authorization: Bearer $APPSCREENSHOTSTUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "iphone-6.9",
    "name": "<app_name> Screenshots",
    "codebase_context": {
      "readme_summary": "...",
      "key_screens": ["..."],
      "color_tokens": {"primary": "#hex"},
      "target_audience": "...",
      "app_category": "...",
      "competitive_edge": "...",
      "ui_style": "...",
      "primary_user_flow": "..."
    }
  }'
```

Save `data.id` as `PROJECT_ID`.

**3b. Generate the screenshot set via chat:**

```bash
curl -s -X POST "https://appscreenshotstudio.com/api/v1/projects/$PROJECT_ID/chat" \
  -H "Authorization: Bearer $APPSCREENSHOTSTUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a 5-card screenshot set. Highlight: [feature1], [feature2], [feature3]. Mood: minimal. Use brand color #hex."
  }'
```

On success, `data.canvas_state` contains the generated layout. The response also includes `data.message` (Claude's description of what was created) and `credits_remaining`.

If `data.operations` is empty, Claude asked a clarifying question — no credits were deducted. Answer the question and call chat again.

### Step 4 — Iterate if needed

If the user wants changes, call chat again on the same `PROJECT_ID`:

```bash
curl -s -X POST "https://appscreenshotstudio.com/api/v1/projects/$PROJECT_ID/chat" \
  -H "Authorization: Bearer $APPSCREENSHOTSTUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Make the first card more playful. Change the headline to something punchier."}'
```

### Step 5 — Render and export

Render the final PNGs at exact App Store dimensions (free, no credits):

```bash
curl -s -X POST "https://appscreenshotstudio.com/api/v1/projects/$PROJECT_ID/render" \
  -H "Authorization: Bearer $APPSCREENSHOTSTUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Returns `data.images[]` — array of CDN URLs. Download them or share the project URL:
`https://appscreenshotstudio.com/builder/<PROJECT_ID>`

## Credit costs

- Project creation: free
- Chat (screenshot generation): 5 credits per message
- Render: free
- Clarifying questions (no operations generated): refunded automatically

## Headline quality rules

When reviewing or suggesting headlines, enforce:
- 3–5 words per line, readable at thumbnail size
- Three styles: paint a moment ("Morning runs handled"), state an outcome ("Never miss a workout"), eliminate a pain ("Ditch the spreadsheet")
- Never: feature lists, "and"-joined clauses, starting with "The", vague aspirational phrases

## Error codes

- `NO_CREDITS` (402) — user needs to top up at https://appscreenshotstudio.com/billing
- `PROJECT_LIMIT_REACHED` (403) — plan limit hit
- `UNAUTHORIZED` (401) — invalid or missing API key
- `NOT_FOUND` (404) — project ID doesn't exist
