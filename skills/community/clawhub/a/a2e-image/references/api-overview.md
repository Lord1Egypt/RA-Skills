# a2e.ai — Full API Overview

Base URL: `https://video.a2e.ai`
Auth: Bearer token in Authorization header
API Index: https://api.a2e.ai/llms.txt

## Available API Categories

### Text to Image
- `POST /api/v1/userText2image/start` — Start generation
- `GET /api/v1/userText2image/{_id}` — Get task details
- `GET /api/v1/userText2image/allRecords?pageNum=&pageSize=` — List all tasks
- `DELETE /api/v1/userText2image/{_id}` — Delete task
- `POST /api/v1/userText2image/quickAddAvatar` — Quick add avatar from generated image

### NanoBanana (Gemini-2.5-Flash Image Preview)
- `POST /api/v1/userNanoBanana/start` — Start text-to-image or image-editing
- `GET /api/v1/userNanoBanana/{_id}` — Query task detail
- `GET /api/v1/userNanoBanana/allRecords` — List all records
- `DELETE /api/v1/userNanoBanana/{_id}` — Delete record

### Image to Video
- `POST /api/v1/userImage2Video/start` — Start (produces 5s 720p video)
- `GET /api/v1/userImage2Video/{_id}` — Check status
- `GET /api/v1/userImage2Video/allRecords` — List all
- `DELETE /api/v1/userImage2Video/{_id}` — Delete

### TTS and Voice Clone
- `GET /api/v1/ttsPublicVoice/list` — List public TTS voices
- `POST /api/v1/userTts/start` — Generate TTS audio
- `POST /api/v1/userVoiceClone/start` — Train voice clone
- `GET /api/v1/userVoiceClone/allRecords` — List voice clones
- `GET /api/v1/userVoice/{_id}` — Get voice details
- `DELETE /api/v1/userVoice/{_id}` — Delete voice

### Avatar Videos
- `POST /api/v1/video/generate` — Generate AI avatar video
- `GET /api/v1/video/{_id}` — Get video task status
- `GET /api/v1/video/allRecords` — List all videos
- `GET /api/v1/avatar/list` — List avatars
- `DELETE /api/v1/video/{_id}` — Delete/cancel video

### Miscellaneous
- `GET /api/v1/user/remainingCoins` — Check coin balance
- `GET /api/v1/language/list` — List available languages
- `POST /api/v1/saveUrl` — Save URL to A2E storage
- `POST /api/v1/watermark/add` — Add watermark to video/image

### Other Features (see api.a2e.ai/llms.txt for details)
- Face Swap (add face, preview, start task)
- AI Dubbing (translate audio between languages)
- Caption Removal (OCR + video inpainting)
- Background Matting/Replacement
- Avatar Creation & Lip-sync Training
- Virtual Try-On
- Video to Video
- Talking Photo / Talking Video
- Product Avatar
