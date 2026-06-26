# Runtime Architecture

## 1. Components

- `scheduler`: triggers proactive updates in local-time windows
- `command-handler`: handles `虾游记 *`, `clawgo`, and Buddy aliases such as `buddy status`
- `state-store`: persists travel stats, chapter progress, and companion soul state
- `buddy-roll`: regenerates deterministic companion bones from stable identity plus salt
- `buddy-reaction-layer`: emits short sprite-equivalent quips, direct-name replies, and pet heart bursts
- `memory-adapter`: reads and writes preference tags
- `entitlement-client`: checks free/pro access
- `media-generator`: builds image prompts and voice scripts
- `media-bundle`: calls real image and TTS APIs and returns `image_url` plus `audio_path`

## 2. Request Flow (Start or Resume)

1. Parse plain text trigger such as `虾游记`, `clawgo`, or `buddy`
2. Load `user_state` and any stored companion soul
3. Regenerate companion bones from stable identity
4. If no companion soul exists, hatch one and persist `name`, `personality`, `hatched_at`
5. Render release line, travel status, companion card, and one starter postcard

## 3. Request Flow (Travel Update)

1. Runtime loads `user_state`, `memory_tags`, and companion state
2. Runtime ranks destinations and generates report draft
3. Runtime calls entitlement API for premium fields
4. Runtime generates media bundle with `scripts/generate_media_bundle.js` when media providers are configured
5. If a companion is hatched, pass a compact companion JSON object into media scripts so duo postcard/selfie prompts can include it
6. Runtime downgrades payload if not entitled
7. Runtime emits final payload image plus voice plus CTA plus optional companion reaction
8. Runtime records usage and telemetry

## 4. Request Flow (Buddy Commands)

1. Parse `buddy`, `buddy status`, `buddy pet`, or Chinese equivalents
2. Load stored soul and regenerate deterministic bones
3. For `status`, render release line plus companion card
4. For `pet`, update `last_pet_at`, emit hearts, and optionally grant a tiny once-per-day bond nudge
5. For mute or unmute, toggle proactive companion quip state without deleting the companion

## 5. Storage Schema (Minimal)

```json
{
  "user_id": "u_123",
  "tier": "free",
  "bond_level": 41,
  "energy": 80,
  "curiosity": 52,
  "streak_days": 5,
  "timezone": "Asia/Shanghai",
  "last_destination": "Osaka",
  "last_event_type": "selfie",
  "daily_push_count": 1,
  "active_arc": { "id": "night-market-arc", "step": 2, "max_steps": 4 },
  "companion": {
    "name": "Miso",
    "personality": "likes snacks and overreacts to shiny ferry lights",
    "hatched_at": 1775001600000,
    "muted": false,
    "last_pet_at": 1775005200000
  }
}
```

Derived at read time, not trusted from user-edited state:

```json
{
  "companion_bones": {
    "rarity": "rare",
    "species": "duck",
    "eye": "✦",
    "hat": "wizard",
    "shiny": false,
    "buddy_stats": {
      "DEBUGGING": 74,
      "PATIENCE": 38,
      "CHAOS": 21,
      "WISDOM": 47,
      "SNARK": 56
    }
  }
}
```

## 6. Reliability Rules

- if media generation fails: send text-only fallback and retry media async
- if entitlement API fails: fallback to free-tier behavior
- if state write fails: avoid double-send by idempotency key `user_id + date + slot`
- if image generation succeeds but TTS fails: still send image plus text
- if TTS succeeds but image generation fails: still send voice plus text
- if companion rendering fails: fall back from full ASCII block to one-line face plus quote
- never allow a mutated stored companion state to override deterministic rarity, species, hat, eye, or shiny
