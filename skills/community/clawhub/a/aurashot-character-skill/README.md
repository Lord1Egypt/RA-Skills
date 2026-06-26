# AuraShot Character Skill

Character-consistent AI image generation for your agent. Same person, any outfit, any scene, every time.

Upload one face photo — the engine locks the character's facial features, skin tone, hairstyle, and identity, then preserves it across unlimited generations. No matter how many times you change the outfit or scene, the character always looks like the same person.

## What It Does

- **ID Photo**: Generate a 4-in-1 identity baseline from any face photo
- **Generate**: Create new character images with outfit, scene, and pose references
- **Edit**: Modify existing images with natural language instructions
- **Multi-Character**: Manage multiple characters with local directory structure

Works with real-person photos and anime/virtual characters.

## Quick Start

```bash
# Install
clawhub install aurashot-character-skill

# Set your API key (free tier available)
echo 'AURASHOT_API_KEY=sk_live_YOUR_KEY' > .aurashot.env

# Generate an ID photo
python3 scripts/aurashot.py id-photo --face-image photo.jpg --output avatars/Snow/profile --wait

# Generate a scene
python3 scripts/aurashot.py character-generate --face-image avatars/Snow/profile/id-photo.png --description "wearing a red gown on stage" --output avatars/Snow/gallery --wait

# Edit an image
python3 scripts/aurashot.py edit --target-image avatars/Snow/gallery/result.png --description "change to a side pose" --output avatars/Snow/gallery --wait
```

## Get Your API Key

1. Sign up at [aurashot.art](https://www.aurashot.art/login)
2. Get your key at [Studio → API Keys](https://www.aurashot.art/studio?tab=keys)

Free tier included. Upgrade for more quota at [Studio → Billing](https://www.aurashot.art/studio?tab=billing).

## Requirements

- Python 3
- `AURASHOT_API_KEY` environment variable or `.aurashot.env` file

## Links

- [Homepage](https://www.aurashot.art)
- [API Documentation](https://www.aurashot.art/studio?tab=docs)
- [ClawHub](https://clawhub.ai/whbzju/aurashot-character-skill)
