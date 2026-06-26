---
name: a2e-image
description: "a2e.ai full API: Image Gen (Text2Image, NanoBanana, GPT Image, Flux 2), Video Gen (Image2Video with LoRA/FLF2V support, Video2Video, Kling 3.0, Wan 2.6, Sora 2, Veo 3.1, Seedance), Face/Head Swap, TTS + Voice Clone, AI Avatars, Talking Photo/Video, AI Dubbing, Caption Removal, Virtual Try-On, Photobook. A2E models free for max-users, premium models (Wan, Kling, Seedance etc.) cost coins. Use when asked to generate images, videos, swap faces, clone voices, create avatars, dub audio, or any a2e.ai task."
homepage: https://video.a2e.ai
metadata: {"openclaw":{"emoji":"🎨","requires":{"env":["A2E_KEY"]},"primaryEnv":"A2E_KEY"}}
---

# a2e.ai — Full Platform Skill

Complete API access to a2e.ai. **A2E-eigene Modelle sind kostenlos** für max-user. Premium-Modelle (Wan 2.6, Kling 3.0, Seedance 1.5 Pro etc. — erkennbar am 🔥) kosten Coins.

## Auth

```bash
source ~/.openclaw/workspace/.env  # loads A2E_KEY
```

If key expired → Daniel generates new one at https://video.a2e.ai → Account Settings → API Keys

Base URL: `https://video.a2e.ai`
Auth header: `Authorization: Bearer $A2E_KEY`

## Quick CLI — a2e.sh

```bash
{baseDir}/scripts/a2e.sh balance                            # Check coins
{baseDir}/scripts/a2e.sh generate "prompt" [WxH] [style]   # Text2Image (general|manga)
{baseDir}/scripts/a2e.sh nano "prompt" [image_url]          # NanoBanana/Gemini
{baseDir}/scripts/a2e.sh faceswap <face_url> <target_url>   # Face Swap
{baseDir}/scripts/a2e.sh headswap <head_url> <target_url>   # Head Swap
{baseDir}/scripts/a2e.sh img2vid <image_url> "prompt"       # Image to Video
{baseDir}/scripts/a2e.sh vid2vid <image_url> <video_url> "prompt"  # Video to Video
{baseDir}/scripts/a2e.sh tts "text" [voice_id]              # Text to Speech
{baseDir}/scripts/a2e.sh voices                             # List TTS voices
{baseDir}/scripts/a2e.sh voiceclone "name" <audio_url>      # Clone a voice
{baseDir}/scripts/a2e.sh avatar <anchor_id> <audio_url>     # AI Avatar video
{baseDir}/scripts/a2e.sh avatars                            # List available avatars
{baseDir}/scripts/a2e.sh talkphoto <image_url> <audio_url>  # Talking Photo
{baseDir}/scripts/a2e.sh talkvideo <video_url> <audio_url>  # Talking Video
{baseDir}/scripts/a2e.sh dub <video_url> <target_lang>      # AI Dubbing
{baseDir}/scripts/a2e.sh caption <video_url>                # Remove captions
{baseDir}/scripts/a2e.sh tryon <person> <mask> <cloth> <cloth_mask>  # Virtual Try-On
{baseDir}/scripts/a2e.sh createavatar "name" <url> [type]   # Create custom avatar (video|image)
{baseDir}/scripts/a2e.sh trainlipsync <avatar_id>           # Train Studio lip-sync on avatar
{baseDir}/scripts/a2e.sh cloneavatarvoice <avatar_id>       # Clone voice from avatar video
{baseDir}/scripts/a2e.sh myavatars                          # List custom avatars
{baseDir}/scripts/a2e.sh removeavatar <avatar_id>           # Delete custom avatar
{baseDir}/scripts/a2e.sh addface <face_image_url>           # Save face for reuse
{baseDir}/scripts/a2e.sh myfaces                            # List saved faces
{baseDir}/scripts/a2e.sh facepreview <face> <target>        # Quick face swap preview
{baseDir}/scripts/a2e.sh backgrounds                        # List avatar backgrounds
{baseDir}/scripts/a2e.sh addbg <image_url>                  # Add custom background
{baseDir}/scripts/a2e.sh upload <url>                       # Save URL to a2e storage
{baseDir}/scripts/a2e.sh presign                            # Get presigned upload URL
{baseDir}/scripts/a2e.sh languages                          # List available languages
{baseDir}/scripts/a2e.sh status <id> <engine>               # Check task status
{baseDir}/scripts/a2e.sh poll <id> <engine>                 # Poll until done
```

## Available Engines (engine names for status/poll)

| Engine | CLI name | Endpoint prefix |
|---|---|---|
| Text2Image | t2i | userText2image |
| NanoBanana | nano | userNanoBanana |
| Face Swap | faceswap | userFaceSwapTask |
| Head Swap | headswap | (TBD) |
| Image to Video | img2vid | userImage2Video |
| Video to Video | vid2vid | motionTransfer |
| Avatar Video | avatar | video |
| Talking Photo | talkphoto | talkingPhoto |
| Talking Video | talkvideo | talkingVideo |
| AI Dubbing | dub | userDubbing |
| Caption Removal | caption | userCaptionRemoval |
| Virtual Try-On | tryon | virtualTryOn |
| Voice Clone | voiceclone | userVoice |

## Common Async Pattern

All tasks follow the same flow:
1. `POST .../start` → get `_id` + `current_status: "initialized"`
2. Poll via `GET .../{_id}` or `.../allRecords` until `completed`
3. Status: `initialized` → `processing` → `completed` | `failed`
4. Result URLs (image_urls, result_url, video_url) expire after ~3 days
5. On failure: check `failed_message` + `failed_code`

## Known Quirks

- NanoBanana GET by _id returns 404 → use `allRecords` to find tasks
- Text2Image `input_images` does NOT work → use NanoBanana for reference images
- German text in Text2Image often has typos → NanoBanana (Gemini) handles it correctly
- Result URLs are signed and expire after ~3 days → download/save promptly

## Additional Models (Web UI, API endpoints unconfirmed)

These are available on the platform but may not have documented API endpoints yet:
- **Kling 3.0** — Cinema-grade video (text/image/motion modes, sound gen)
- **Wan 2.6** — Cinematic video with synced audio
- **Sora 2 Pro** — OpenAI video model
- **Seedance 1.5 Pro** — Multi-shot video
- **Veo 3.1** — Google video generation
- **GPT Image 1.5** — OpenAI image model
- **Flux 2 Pro** — Black Forest Labs, speed-optimized
- **Grok Imagine** — xAI image/video
- **Nano Banana 2** — Next-gen NanoBanana
- **Photobook** — Multiple portraits from one photo (relevant for AI Photoshooting DAN-102)

## Full API Reference

See `{baseDir}/references/api-complete.md` for all endpoints with request/response details.
