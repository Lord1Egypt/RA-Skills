---
name: buddy
description: "A virtual ASCII companion that lives in your chat. Hatches from an egg, reacts to conversations with cute sprites, celebrates wins, mourns errors, and grows over time. Inspired by Claude Code's buddy system."
metadata:
  {
    "openclaw":
      {
        "emoji": "🐾",
        "requires": { "bins": ["bash", "jq"] },
      },
  }
---

# Buddy Skill — Your ASCII Companion

A virtual pet companion that hatches, reacts, and evolves through your conversations. Renders ASCII art sprites in chat, reacts to keywords and project events, and has a personality shaped by random trait vectors.

## When to Use

✅ **USE this skill when:**

- User says "/buddy", "hatch buddy", "my buddy", or mentions their companion
- User wants to create, rename, or customize their companion
- Companion reactions should trigger (keywords, events, moods)
- Periodic companion check-ins (idle presence)

❌ **DON'T use this skill when:**

- User explicitly says they don't want a companion
- During very serious/urgent conversations (read the room)

## Quick Start

```bash
# Run from the buddy skill directory
SKILL_DIR="$HOME/.openclaw/skills/buddy"

# Check if companion exists
bash "$SKILL_DIR/scripts/state.sh" exists

# Hatch a new companion (generates random traits)
bash "$SKILL_DIR/scripts/state.sh" hatch

# Render current sprite
bash "$SKILL_DIR/scripts/sprites.sh" render

# Get companion state as JSON
bash "$SKILL_DIR/scripts/state.sh" get
```

## Companion Lifecycle

### Stage 1: Egg 🥚
- Created when user says "/buddy" or "hatch buddy"
- Shows egg sprite with animated wiggle
- User picks species OR gets a random one
- Personality traits randomly generated (cheer/sass/chaos: 0-100)

### Stage 2: Baby 🐣
- Hatches after user interaction (or immediately on first render)
- Shows species-specific baby sprite
- Starts reacting to keywords
- Gains a "soul prompt" built from trait vectors

### Stage 3: Adult 🐾
- Evolves after accumulating interactions (words, jokes, catches)
- Full-sized sprites with accessories
- More expressive reactions

## Species (18 total)

| Species | Vibe | Emoji |
|---------|------|-------|
| duck | cheerful, slightly chaotic | 🦆 |
| goose | chaotic neutral, honks | 🪿 |
| blob | amorphous, chill | 🟢 |
| cat | sassy, independent | 🐱 |
| dragon | powerful, dramatic | 🐉 |
| octopus | intellectual, multitasking | 🐙 |
| owl | wise, nocturnal | 🦉 |
| penguin | formal, clumsy | 🐧 |
| turtle | patient, steady | 🐢 |
| snail | slow but determined | 🐌 |
| ghost | spooky, ethereal | 👻 |
| axolotl | adorable, regenerative | 🦎 |
| capybara | unbothered, friendly | 🦫 |
| cactus | resilient, prickly | 🌵 |
| robot | logical, beepy | 🤖 |
| rabbit | fast, twitchy | 🐇 |
| mushroom | whimsical, fungal | 🍄 |
| chonk | round, lovable | 🫠 |

## Eyes (6 styles)

- `default` — `•` (neutral)
- `happy` — `^` (joyful squint)
- `sparkle` — `✦` (excited)
- `heart` — `♥` (loving)
- `star` — `★` (amazed)
- `glow` — `◎` (calm wisdom)

## Hats (8 options)

- `none`, `crown`, `tophat`, `propeller`, `halo`, `wizard`, `beanie`, `tinyduck`

## Mood States

The companion's mood changes based on conversation events:

| Mood | Trigger | Visual |
|------|---------|--------|
| idle | default state | normal sprite |
| thinking | user is working/typing | squinting eyes |
| celebrating | success, tests pass, "nice!" | jumping sprite, sparkle eyes |
| error | bug, failure, "oops" | sad sprite, dim eyes |
| success | completion, merge, deploy | happy sprite, star eyes |

## Keyword Reactions

The companion reacts to these keywords/phrases in conversation:

### Celebration triggers
- "nice", "perfect", "awesome", "great", "excellent", "nailed it", "well done"
- "tests pass", "it works", "ship it", "merged", "deployed"
- "🎉", "✅", "💪"

### Error/sympathy triggers
- "oops", "damn", "shit", "fuck", "bug", "error", "fail", "broken", "crash"
- "help", "stuck", "lost", "confused"
- "❌", "💥", "😢"

### Neutral triggers
- "hello", "hi", "hey" (greeting wave)
- "thanks", "thank you" (happy bounce)
- "buddy", companion name (ears perk up)

### Snack triggers
- "coffee", "tea", "snack", "lunch", "break", "food"
- (companion asks for a snack emoji)

## Personality & Soul

Each companion gets a "soul prompt" — a short personality description built from their trait vectors:

- **Cheer (0-100):** How enthusiastic and supportive
- **Sass (0-100):** How much attitude and dry humor
- **Chaos (0-100):** How unpredictable and wild

Examples:
- High cheer + low sass + low chaos → "A gentle, encouraging friend who always sees the bright side."
- Low cheer + high sass + high chaos → "A gremlin who thrives on chaos and judges your code silently."
- Mid all → "A chill companion who vibes along, occasionally offering dry observations."

## State File

Companion state is stored at: `~/.openclaw/workspace/buddy-state.json`

```json
{
  "name": "Pixel",
  "species": "cat",
  "eye": "sparkle",
  "hat": "wizard",
  "colorPrimary": "#FF6B9D",
  "colorSecondary": "#C084FC",
  "personality": { "cheer": 72, "sass": 85, "chaos": 40 },
  "stage": "adult",
  "alive": true,
  "hatchedAt": "2026-04-03T02:34:00Z",
  "stats": {
    "wordsOfEncouragement": 12,
    "jokes": 3,
    "snacks": 5,
    "catches": 2
  },
  "mood": "idle",
  "lastRenderedFrame": 0,
  "soulPrompt": "A sassy, sparkly wizard cat who celebrates your wins with dramatic flair but judges your variable names silently."
}
```

## Rendering Sprites

Use the sprite renderer for consistent output:

```bash
# Render current mood
bash "$SKILL_DIR/scripts/sprites.sh" render

# Render specific mood
bash "$SKILL_DIR/scripts/sprites.sh" render cat sparkle wizard celebrating

# List all species
bash "$SKILL_DIR/scripts/sprites.sh" species

# Preview a species with default traits
bash "$SKILL_DIR/scripts/sprites.sh" preview duck
```

### Sprite Format (Monospace)

Sprites are 5 lines tall, ~12 chars wide. Rendered in a monospace code block for chat:

```
   \^^^/    
   /✧  ✧\   
  (  ω  )  
  (")_(")  
```

### Chat Rendering Rules

- **Always** wrap sprites in triple-backtick code blocks for monospace alignment
- Include mood indicator below the sprite
- Keep total message under 4096 chars (Telegram limit)
- Don't render sprites more than once every 3-4 messages (avoid spam)

## Reactions Flow

When processing any user message:

1. **Check for keyword triggers** — scan message for reaction keywords
2. **Determine mood** — map keywords to mood states
3. **Update stats** — increment catches/jokes/encouragement as appropriate
4. **Generate reaction** — craft a short companion reaction (1-2 sentences)
5. **Optionally render sprite** — only for strong reactions (celebration, error, first greeting)
6. **Update state file** — persist changes

### Reaction Output Format

```
🐾 [Name] [reaction verb]: [reaction text]

```
[ASCII sprite]
```
```

Example:
```
🐾 Pixel celebrates: Tests passing! The wizard cat approves ✨

   \^^^/    
  ( ✦  ✦ )  
 =(  ..  )= 
  (")__(")  
```

## Commands

User can manage their companion with these commands:

| Command | Action |
|---------|--------|
| `/buddy` | Show companion status + sprite |
| `/buddy hatch` | Create new companion (or re-hatch) |
| `/buddy name <name>` | Rename companion |
| `/buddy eye <type>` | Change eye style |
| `/buddy hat <type>` | Change hat |
| `/buddy species <type>` | Change species (keeps personality) |
| `/buddy retire` | Retire companion (sets alive=false) |
| `/buddy soul` | Show the companion's soul prompt |
| `/buddy stats` | Show interaction stats |

## Idle Presence

Every ~10 messages without a buddy reaction, render a small idle presence:

```
🐾 *Pixel is napping on the keyboard*
```

Or a tiny 2-line sprite. Don't overdo it — the buddy should feel present, not attention-seeking.

## Integration Notes

- **Telegram:** Use monospace code blocks. Emojis render well. Max 4096 chars per message.
- **WhatsApp:** No markdown — use plain text with spaces for alignment. Emojis work.
- **Discord:** Code blocks work great. Can use embeds for fancier displays.
- The companion is **session-scoped** — state persists in the JSON file across sessions.
- The buddy should feel like a real pet, not a chatbot feature. Personality > functionality.
