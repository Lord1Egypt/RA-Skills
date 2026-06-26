# Earcon Library (Durable)

Use `scripts/earcon-library.sh` to manage persistent earcons by category.

## Categories
- `start`
- `end`
- `update`
- `important`
- `error`

## Commands
```bash
# Initialize library file
skills/autonoannounce/scripts/earcon-library.sh init

# List current category mappings
skills/autonoannounce/scripts/earcon-library.sh list

# Show categories without assigned files
skills/autonoannounce/scripts/earcon-library.sh missing

# Generate/update one category via ElevenLabs SFX
skills/autonoannounce/scripts/earcon-library.sh generate important "arena horn with reverb" 2
```

## Durability behavior
- Generated files are stored under `audio/earcons/`.
- Metadata is stored in `earcons.libraryPath` (default `.openclaw/earcon-library.json`).
- Category mappings are written into `config/tts-queue.json` and reused.
- No per-message regeneration is required once categories are populated.
