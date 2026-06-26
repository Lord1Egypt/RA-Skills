---
name: avatar-cog
description: "AI avatar and digital persona creation powered by CellCog. Character.ai for agents — create characters, clone voices, generate images, build personalities. Persistent avatars reusable across all chats. Brand mascots, digital twins, creative characters, AI spokespersons, podcast hosts. Describe your character in plain language and CellCog builds it."
metadata:
  openclaw:
    emoji: "🎭"
    os: [darwin, linux, windows]
    requires:
      bins: [python3]
      env: [CELLCOG_API_KEY]
author: CellCog
homepage: https://cellcog.ai
dependencies: [cellcog]
---
# Avatar Cog - Character.ai for Agents

Create persistent digital personas with images, cloned voices, and personalities — then use them across every CellCog chat. Describe a character in plain language and CellCog builds it.

## Why Avatars

Avatars are persistent characters stored on CellCog. Create once, use everywhere:

- **Brand Mascots**: A consistent character for all your marketing content
- **Digital Twins**: Clone your voice and likeness for AI-generated content
- **Creative Characters**: Fictional personas for stories, comics, videos
- **AI Spokespersons**: Lip-synced video presenters with cloned voices
- **Podcast Hosts**: Consistent voice and personality across episodes

Every CellCog chat automatically sees all your avatars. No setup, no configuration — just reference them by name.

## How to Use

For your first CellCog task in a session, read the **cellcog** skill for the full SDK reference — file handling, chat modes, timeouts, and more.

**OpenClaw (fire-and-forget):**
```python
result = client.create_chat(
    prompt="[your task prompt]",
    notify_session_key="agent:main:main",
    task_label="my-task",
    chat_mode="agent",
)
```

**All agents except OpenClaw (blocks until done):**
```python
from cellcog import CellCogClient
client = CellCogClient(agent_provider="openclaw|cursor|claude-code|codex|...")
result = client.create_chat(
    prompt="[your task prompt]",
    task_label="my-task",
    chat_mode="agent",
)
print(result["message"])
```

---

## What You Can Do

### Create an Avatar

Describe the character you want. CellCog handles the rest:

```
Create an avatar named "Captain Grumbleton" — a grumpy but lovable pirate captain.
He's a brand mascot for a seafood restaurant chain.
Personality: witty, sarcastic, secretly kind-hearted.
Platforms: social media, video content, marketing.
```

CellCog creates the avatar with name, personality traits, use case, and platform configuration.

### Add Images

Generate or provide images for your avatar:

```
Generate a professional headshot for my avatar "Captain Grumbleton" —
cartoon style, pirate hat, bushy beard, one gold tooth, friendly scowl.
Add it as the primary image.
```

Or reference existing files:

```
Add this image to my avatar "Luna":
<SHOW_FILE>/path/to/luna_headshot.png</SHOW_FILE>
Label it "Professional Headshot".
```

Up to 10 images per avatar. These become reference images for all future content generation — CellCog maintains character consistency automatically.

### Clone a Voice

Upload an audio sample and CellCog clones the voice:

```
Clone a voice for my avatar "Luna" using this audio sample:
<SHOW_FILE>/path/to/voice_sample.mp3</SHOW_FILE>
```

Supported formats: MP3, WAV, OGG, M4A, AAC, WebM. The cloned voice is immediately ready for text-to-speech generation via MiniMax Speech 2.8 HD.

### Use Avatars for Content

Once created, just mention the avatar by name in any CellCog chat:

- **"Create a marketing video with Captain Grumbleton introducing our new menu"**
- **"Generate a podcast episode where Luna interviews an expert about AI"**
- **"Create 5 Instagram posts featuring Captain Grumbleton at different restaurants"**
- **"Record a voiceover as Luna for our product demo"**

CellCog automatically retrieves the avatar's images, voice, and personality to create consistent, personalized content.

### List and Manage Avatars

```
Show me all my avatars
```

```
Update my avatar "Luna" — change her personality to be more energetic and add "podcasts" to her platforms
```

```
Delete the image labeled "Old Logo" from Captain Grumbleton
```

```
Delete the voice from my avatar "Luna" — I want to re-record it
```

Everything is natural language. No APIs, no JSON, no tool names — just describe what you want.

---

## How Avatars Work Across Chats

Avatars are **account-level**, not chat-level:

1. **Create once**: Build an avatar in any CellCog chat
2. **Available everywhere**: Every new chat automatically sees all your avatars
3. **Consistent identity**: Same images, voice, and personality in every context
4. **Always up-to-date**: Add an image in one chat, it's available in all chats immediately (next message)

This is the key advantage — your characters are persistent and portable. No re-uploading, no re-describing.

---

## Avatar + Content Creation Workflows

### Marketing Video with Avatar Spokesperson

```
Create a 30-second product intro video with my avatar "Luna" as the spokesperson.
She should introduce our new AI writing tool, highlight three key features,
and close with a call-to-action. Use her cloned voice and professional headshot.
Background music: upbeat corporate.
```

CellCog handles: script writing (aligned to Luna's personality) → speech generation (Luna's cloned voice) → scene creation (Luna's reference images) → video production → music scoring → final edit.

### Social Media Content Series

```
Create 5 Instagram posts featuring Captain Grumbleton:
1. Grumbleton taste-testing a new dish (excited expression)
2. Grumbleton at the helm of a restaurant (captain pose)
3. Grumbleton with a customer (reluctantly friendly)
4. Grumbleton reviewing a competitor (grumpy face)
5. Grumbleton celebrating an award (trying not to smile)
Write captions that match his sarcastic personality.
```

### Podcast with Avatar Host

```
Create a 5-minute podcast episode where Luna discusses the latest AI news.
Use her cloned voice. Add intro music, outro music, and a brief welcome.
Style: conversational, informative, matching Luna's personality.
```

### Multi-Avatar Story

```
Create a comic strip with Captain Grumbleton and Luna having a debate
about whether AI will replace pirate captains. 4 panels.
Grumbleton is skeptical, Luna is optimistic. Both stay in character.
```

---

## Chat Mode

**Use `chat_mode="agent"`** for all avatar tasks. Avatar creation, voice cloning, and content generation all work efficiently in agent mode.

For complex multi-avatar video productions, `chat_mode="agent team"` may provide better results through deeper planning.

---

## Tips

1. **Be descriptive when creating**: The more detail you give about personality, appearance, and use case, the better CellCog can create consistent content
2. **Add multiple images**: Different poses, expressions, and outfits give CellCog more reference material for variety
3. **Voice samples matter**: Clean, 10-30 second audio samples produce the best voice clones. Minimize background noise.
4. **Name your avatars distinctly**: CellCog identifies avatars by name across chats — unique names prevent confusion
5. **Iterate naturally**: "Make Grumbleton's personality more sarcastic" or "Add a holiday outfit image to Luna" — just describe what you want changed

---

## If CellCog is not installed

Run `/cellcog-setup` (or `/cellcog:cellcog-setup` depending on your tool) to install and authenticate.
**OpenClaw users:** Run `clawhub install cellcog` instead.
**Manual setup:** `pip install -U cellcog` and set `CELLCOG_API_KEY`. See the **cellcog** skill for SDK reference.
