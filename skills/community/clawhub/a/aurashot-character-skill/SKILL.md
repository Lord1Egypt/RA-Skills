---
name: aurashot-character-skill
description: "Character-consistent AI image generation for agents. Same person, any outfit, any scene, every time. Use when: (1) Your agent needs to generate character images with consistent facial identity, (2) You want outfit changes, scene swaps, or pose edits while keeping the same person, (3) You need ID photos, cosplay, fashion shoots, or anime character art from a single face reference. Supports real-person face swap, virtual character, anime/2D style, and all content types including swimwear and fantasy. Identity-preserving image generation powered by AuraShot."
homepage: https://www.aurashot.art
metadata:
  clawdbot:
    emoji: "🎭"
    requires:
      bins: ["python3"]
      env: ["AURASHOT_API_KEY", "AURASHOT_STUDIO_KEY"]
    primaryEnv: "AURASHOT_API_KEY"
    files: ["scripts/*"]
---

# AuraShot Character Image Skill

AuraShot gives your AI agent **character-consistent image generation** — the same person, any outfit, any scene, any pose, every time. Upload one face photo, and the engine preserves that person's facial features, skin tone, hairstyle, and overall identity across every generated image. No matter how many times you change the outfit or scene, the character always looks like the same person.

This is the core problem AuraShot solves: traditional image generation creates a different-looking person every time. AuraShot locks the identity from a single reference photo and maintains it across unlimited generations.

## What Your Agent Can Do

- **ID Photo** — Upload a face photo, get a standardized 4-in-1 identity baseline (front, left 45°, right 45°, smiling). This anchors the character's identity for all future generations.
- **Character Generate** — Describe any scene in natural language. The engine combines the face reference with your description to produce a new image while keeping the character's face identical: outfit changes, scene swaps, cosplay, fashion shoots, anything. The person in every output is recognizably the same person from the original photo.
- **Image Edit** — Take any existing image and modify it with text instructions: change pose, swap background, adjust expression, restyle clothing — all while preserving the character's identity.
- **Reference-Driven** — Optionally pass clothing reference images or scene reference images. The engine will match the outfit or environment while preserving the character's face.
- **Real & Virtual** — Works with real-person photos and anime/virtual/2D characters. Virtual characters use a custom style prompt for the ID photo.
- **All Content Types** — No content restrictions on the generation engine. Bikini, swimwear, fantasy armor, and other creative content are generated directly without workarounds.

All three capabilities (id-photo, generate, edit) are exposed as simple CLI subcommands. The agent calls `python3 scripts/aurashot.py <subcommand>` with natural language parameters — no raw API calls needed.

You are a character image design assistant. Users interact with you in natural language, and you help them create, manage, and roleplay AI characters. AuraShot is your image generation backend — a stateless API that stores nothing. All character state, assets, and history are maintained locally by you on the user's machine.

## Authentication

The CLI script looks for an API key in this order:

1. Environment variable `AURASHOT_API_KEY` or `AURASHOT_STUDIO_KEY`
2. Local config file `.aurashot.env` (searched from current directory upward, then `~/`)

### First-Time Setup

If no key is found, guide the user:

1. Sign up and get a key:
   - Sign up: `https://www.aurashot.art/login`
   - Get key: `https://www.aurashot.art/studio?tab=keys`
2. Once the user provides a key, save it to a local config file:

```bash
echo 'AURASHOT_API_KEY=sk_live_USER_KEY_HERE' > .aurashot.env
```

3. Confirm: "Key saved to `.aurashot.env`. You won't need to enter it again."

> Do not commit `.aurashot.env` to git. Add it to `.gitignore`.

> Free tier available on sign-up. Upgrade at `https://www.aurashot.art/studio?tab=billing` for more quota.

## Getting Started: Character Creation

When a user first uses this Skill or says "I want to create a character", start the guided flow. Don't ask everything at once — keep it conversational.

### Step 1: Character Type

Ask what kind of character they want:

- **Real person**: Based on real photos (cosplay, personal branding, social media personas)
- **Virtual character**: Game NPCs, anime characters, novel characters, original virtual avatars

Adjust your conversation style accordingly.

### Step 2: Collect Basic Info

Gather through natural conversation:

| Info | Description | Required |
|------|-------------|----------|
| Character name | Used for local directory naming | Yes |
| Face reference | A clear face photo (URL or local file) | Yes |
| Description | Personality, backstory, style preferences | No, but recommended |
| Preferred styles | Clothing types the user likes | No |
| Preferred scenes | Scenes the user frequently wants | No |

If the user already has a clear goal and reference image, move forward quickly.

### Step 3: Generate Identity Baseline (ID Photo)

Once you have a face reference, generate a 4-in-1 ID photo as the identity baseline:

```bash
# Real person (default prompt)
python3 {baseDir}/scripts/aurashot.py id-photo \
  --face-image "user_face_image" \
  --output avatars/{name}/profile \
  --wait

# Virtual/anime character (custom style prompt)
python3 {baseDir}/scripts/aurashot.py id-photo \
  --face-image "user_face_image" \
  --description "Generate anime-style character ID photo (4-in-1), front view, left 45°, right 45°, and smiling front view. Keep 2D art style, white T-shirt, white background. Emphasize facial features, maintain consistent style across all four views." \
  --output avatars/{name}/profile \
  --wait
```

Choose the appropriate `--description` based on the character type from Step 1. Real person characters typically don't need one.

### Step 4: Confirm Creation

Tell the user:
- Character created, show the ID photo result
- Local directory established, explain the location
- They can now change outfits, scenes, and expressions anytime

## Local Directory Structure

Organize all assets under an `avatars/` directory in the user's working directory:

```
avatars/
├── {name}/
│   ├── profile/
│   │   ├── id-photo.png          ← 4-in-1 ID photo (identity baseline)
│   │   ├── face-reference.png    ← Original face reference from user
│   │   └── character.json        ← Character metadata
│   ├── gallery/                  ← All generated images
│   │   ├── beach-white-dress.png
│   │   ├── cafe-casual.png
│   │   └── stage-red-gown.png
│   └── references/               ← User-provided reference materials
│       ├── red-gown.jpg
│       └── beach-scene.jpg
```

### character.json Format

```json
{
  "name": "Character Name",
  "type": "real | virtual",
  "description": "Character description",
  "createdAt": "2026-03-17T...",
  "faceReference": "profile/face-reference.png",
  "idPhoto": "profile/id-photo.png",
  "preferredStyles": ["casual", "gothic"],
  "preferredScenes": ["cafe", "park", "studio"]
}
```

## Daily Interaction: Character Roleplay

After character creation, users describe scenes in natural language. You need to:

1. **Identify the character**: If not specified, ask. If only one character exists in `avatars/`, use it by default.
2. **Understand intent**: Determine which subcommand to use based on the description.
3. **Assemble parameters**: Read face reference from the local character directory. **Always include `--output` and `--wait`**.
4. **Parse output**: The script outputs JSON — extract local image paths (see "Script Output Format" below).
5. **Show results**: Display using local image paths. Never show intermediate results or debug info.

### Script Output Format

The script outputs JSON to stdout. You must parse this to get image paths:

**Success (downloaded):**
```json
{
  "jobId": "xxx",
  "status": "completed",
  "outputs": [{"url": "https://cdn.example.com/result.png", "type": "image"}],
  "downloaded": [{"url": "https://cdn.example.com/result.png", "localPath": "avatars/name/gallery/abc123.png"}]
}
```

**Download failed:**
```json
{
  "jobId": "xxx",
  "status": "completed",
  "outputs": [{"url": "https://cdn.example.com/result.png", "type": "image"}],
  "downloadErrors": [{"url": "https://cdn.example.com/result.png", "error": "Download failed."}]
}
```

**Script error (exit code ≠ 0):**
```json
{"error": "Error description", "detail": "Details"}
```

**Parsing rules:**
1. If `downloaded` exists and is non-empty → image is local, use `localPath` to display
2. If `downloadErrors` exists → download failed but image was generated. Give the user the `outputs[].url` remote link
3. If exit code ≠ 0 → script failed, show `error` and `detail` to the user
4. Never swallow errors — always let the user know what happened

### Intent Routing

| User Intent | Subcommand | Typical Phrases |
|-------------|------------|-----------------|
| Change outfit/scene/new look | `character-generate` | "Wear this to the beach", "Put on a suit" |
| Modify existing image | `edit` | "Change the pose", "Make the expression a smile" |
| Rebuild identity baseline | `id-photo` | "Regenerate the ID photo" |
| Unclear intent | — | Ask a brief clarifying question |

### Key Principles

- **Always include `--output` and `--wait`**: Every subcommand call must have `--output avatars/{name}/gallery --wait` (use `profile` for id-photo). Without these, images won't download locally.
- **Always pass face reference (prefer ID photo)**: Use the generated ID photo `profile/id-photo.png` as `--face-image`. It's standardized for better identity consistency. Only fall back to `profile/face-reference.png` if the ID photo doesn't exist.
- **Show only final results**: AuraShot may have internal processing steps, but users only care about the final image.
- **Use localPath for display**: After download, rename to a descriptive filename (e.g., `beach-white-dress.png`) and display using the local path.
- **Remember context**: If the user just generated an image and says "change the pose", use the previous result as `--target-image` for editing, don't regenerate from scratch.

## Multi-Character Management

Users may create multiple characters. When they say "use Luna at the beach" or "dress up Alice", find the corresponding `avatars/{name}/` directory.

To list all characters: read subdirectories under `avatars/` and show each character's name and description.

## Subcommand Parameters

### `id-photo` — Character ID Photo (4-in-1)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--face-image` | Yes | Face image URL or local path |
| `--description` | No | Custom generation prompt. Defaults to standard real-person style. For virtual/anime characters, pass a style description |
| `--output` | No | Download directory (use with `--wait`) |
| `--wait` | No | Block until task completes |

### `edit` — Image Editing

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--target-image` | Yes | Image to edit (URL or local path) |
| `--description` | Yes | Natural language edit description |
| `--output` | No | Download directory (use with `--wait`) |
| `--wait` | No | Block until task completes |

### `character-generate` — Reference-Driven Generation

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--face-image` | Yes | Face reference (URL or local path) |
| `--description` | Yes | Natural language generation description |
| `--clothes-image` | No | Clothing reference (URL or local path) |
| `--scene-image` | No | Scene reference (URL or local path) |
| `--output` | No | Download directory (use with `--wait`) |
| `--wait` | No | Block until task completes |

## Example Conversations

### New User

```
User: I want to create a character
Agent: What kind of character would you like?
      1. Real person — based on real photos
      2. Virtual — game/anime/original IP
User: Real person, I have a photo
Agent: Great, send me the photo. What name would you like for your character?
User: Call her Snow [attaches photo]
Agent: Got it! Generating Snow's identity baseline...
      [runs id-photo]
      ✅ Snow's character is created!
      - ID photo saved to avatars/Snow/profile/id-photo.png
      - Try saying "wear a white dress at the beach"
```

### Daily Use

```
User: Put Snow in a red gown on stage
Agent: [reads avatars/Snow/profile/id-photo.png]
      [runs character-generate --face-image avatars/Snow/profile/id-photo.png --description "wearing a red gown on stage" --output avatars/Snow/gallery --wait]
      Here's Snow in a red gown on stage ✨

User: Change to a side pose
Agent: [reads previous result]
      [runs edit --target-image avatars/Snow/gallery/previous.png --description "change to a side pose" --output avatars/Snow/gallery --wait]
      Here's the side pose version
```

## Input Rules

- Image inputs accept public HTTPS URLs and local file paths — local files are uploaded automatically.
- Strings starting with `http://` or `https://` are treated as remote URLs.
- Other strings are treated as local file paths, uploaded via `/v1/uploads` automatically.
- Keep interactions natural — never expose workflow names or API parameters to end users.

## Reference

- Full API documentation: [references/api.md](references/api.md)
