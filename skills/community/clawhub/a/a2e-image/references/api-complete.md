# a2e.ai — Complete API Reference

Base URL: `https://video.a2e.ai`
Auth: `Authorization: Bearer $A2E_KEY`
Source: https://api.a2e.ai/llms.txt

---

## 1. Text to Image

### Start Text-to-Image
```
POST /api/v1/userText2image/start
Body: { name, prompt, req_key, width, height }
req_key: "high_aes_general_v21_L" (General) | "high_aes" (Manga)
Cost: 10-20 coins
```

### Get Task Detail
```
GET /api/v1/userText2image/{_id}
```

### List All Tasks
```
GET /api/v1/userText2image/allRecords?pageNum=1&pageSize=10
```

### Delete Record
```
DELETE /api/v1/userText2image/{_id}
```

---

## 2. NanoBanana (Gemini-2.5-Flash Image)

### Start Task (text-to-image or image-editing)
```
POST /api/v1/userNanoBanana/start
Body: { name, prompt, input_images?: [url, ...] }
Cost: 15-20 coins. No width/height — model decides.
```

### Get Task Detail
```
GET /api/v1/userNanoBanana/{_id}
NOTE: Returns 404 — use allRecords instead to find by _id
```

### List All Records
```
GET /api/v1/userNanoBanana/allRecords?pageNum=1&pageSize=10
Response: { data: { list: [...] } }
```

### Delete Record
```
DELETE /api/v1/userNanoBanana/{_id}
```

---

## 3. Face Swap

### Add Face Swap Image (upload face to use)
```
POST /api/v1/userFaceSwapImage/add
Body: { face_url: "https://..." }
```

### Get Face Swap Images
```
GET /api/v1/userFaceSwapImage/allRecords
```

### Delete Face Swap Image
```
DELETE /api/v1/userFaceSwapImage/{_id}
```

### Start Face Swap Task
```
POST /api/v1/userFaceSwapTask/add
Body: { name, face_url, video_url }
face_url: URL of face image to swap in
video_url: URL of video/image to swap face onto
```

### Get Face Swap Task Status
```
GET /api/v1/userFaceSwapTask/{_id}
```

### List Face Swap Tasks
```
GET /api/v1/userFaceSwapTask/allRecords?pageNum=1&pageSize=10
```

### Get Face Swap Details
```
GET /api/v1/userFaceSwapTask/detail?_id={_id}
```

### Delete Face Swap Task
```
DELETE /api/v1/userFaceSwapTask/{_id}
```

### Quick Preview Face Swap
```
POST /api/v1/userFaceSwapPreview/add
Body: { face_url, video_url }
GET /api/v1/userFaceSwapPreview?_id={_id}
```

---

## 4. TTS & Voice Clone

### List Public TTS Voices
```
GET /api/v1/anchor/voice_list
Returns voice options from Azure + ElevenLabs
```

### Generate TTS Audio
```
POST /api/v1/video/send_tts
Body: { msg, tts_id, speechRate? }
- tts_id: from voice_list (data → children → value)
- speechRate: 1 = normal, higher = faster
Alternative: use user_voice_id + country + region for cloned voice
```

### Train Voice Clone
```
POST /api/v1/userVoice/startTraining
Body: { name, audio_url }
```

### List Voice Clone Options (completed)
```
GET /api/v1/userVoice/completedRecord
```

### List Ongoing Voice Clone Tasks
```
GET /api/v1/userVoice/processingRecord
```

### Get Voice Details
```
GET /api/v1/userVoice/{_id}
```

### Delete Voice
```
DELETE /api/v1/userVoice/{_id}
```

---

## 5. Avatar Videos (Lip-sync)

### Generate AI Avatar Video
```
POST /api/v1/video/generate
Body: {
  title, anchor_id, anchor_type (0=system, 1=custom),
  audioSrc (audio URL), resolution?, back_id?,
  web_bg_width?, web_bg_height?, web_people_width?, web_people_height?,
  isSkipRs? (Smart Motion — better quality but slower)
}
```

### List Result Videos
```
GET /api/v1/video/allRecords?pageNum=1&pageSize=10
```

### List Avatars
```
GET /api/v1/anchor/character_list
```

### Get Video Task Status
```
GET /api/v1/video/{_id}
```

### Delete/Cancel Video
```
DELETE /api/v1/video/{_id}
```

### Auto Language Detect
```
POST /api/v1/video/language_detect
Body: { text }
```

---

## 6. Create Avatars & Train Lip-sync

### Create Custom Avatar (from video or image)
```
POST /api/v1/userVideoTwin/create
Body: { name, video_url | image_url }
```

### Train Personalized Lip-sync (Studio Avatar 💠)
```
POST /api/v1/userVideoTwin/continueTrain
Body: { _id }
```

### Remove Avatar
```
POST /api/v1/userVideoTwin/remove
Body: { _id }
```

### Get All Training Tasks
```
GET /api/v1/userVideoTwin/allRecords
```

### Get Ongoing Training
```
GET /api/v1/userVideoTwin/processingRecord
```

### Get One Task Status
```
GET /api/v1/userVideoTwin/{_id}
```

### Clone Voice from Avatar Video
```
POST /api/v1/userVideoTwin/cloneVoice
Body: { _id }
```

---

## 7. Image to Video

### Start Image-to-Video
```
POST /api/v1/userImage2Video/start
Body: { name, image_url, prompt, negative_prmpt }
Output: 5 sec, 720p video. Optimized for facial details. ~10 min processing.
```

### Check Status
```
GET /api/v1/userImage2Video/{_id}
```

### List All Tasks
```
GET /api/v1/userImage2Video/allRecords?pageNum=1&pageSize=10
```

### Delete
```
DELETE /api/v1/userImage2Video/{_id}
```

---

## 8. Video to Video (Motion Transfer)

### Start Video to Video
```
POST /api/v1/motionTransfer/start
Body: { name, image_url, video_url, positive_prompt, negative_prompt }
```

### List Tasks
```
GET /api/v1/motionTransfer/allRecords?pageNum=1&pageSize=10
```

### Get Details
```
GET /api/v1/motionTransfer/{_id}
```

### Delete
```
DELETE /api/v1/motionTransfer/{_id}
```

---

## 9. Talking Photo

### Start Task
```
POST /api/v1/talkingPhoto/start
Body: { name, image_url, audio_url, duration (1-10 sec), prompt, negative_prompt }
```

### List Tasks
```
GET /api/v1/talkingPhoto/allRecords?pageNum=1&pageSize=10
```

### Get Detail
```
GET /api/v1/talkingPhoto/{_id}
```

### Delete
```
DELETE /api/v1/talkingPhoto/{_id}
```

---

## 10. Talking Video

### Start Task
```
POST /api/v1/talkingVideo/start
Body: { name, video_url, audio_url, prompt, negative_prompt }
```

### List/Get/Delete
```
GET /api/v1/talkingVideo/allRecords
GET /api/v1/talkingVideo/{_id}
DELETE /api/v1/talkingVideo/{_id}
```

---

## 11. AI Dubbing

### Start Dubbing
```
POST /api/v1/userDubbing/startDubbing
Body: { source_url, name, target_lang, source_lang, num_speakers, drop_background_audio }
Languages: zh, en, ar, ja, es, de, fr, etc.
Auto-clones voice from input.
```

### List Tasks
```
GET /api/v1/userDubbing/allRecords?pageNum=1&pageSize=10
```

### List Processing
```
GET /api/v1/userDubbing/processingRecord
```

### Get Details
```
GET /api/v1/userDubbing/detail?_id={_id}
```

### Delete
```
DELETE /api/v1/userDubbing/{_id}
```

---

## 12. Caption Removal

### Start Caption Removal
```
POST /api/v1/userCaptionRemoval/start
Body: { name, video_url }
Uses OCR to detect + inpaint text from video frames.
```

### List/Status/Detail/Delete
```
GET /api/v1/userCaptionRemoval/allRecords?pageNum=1&pageSize=10
GET /api/v1/userCaptionRemoval/processingRecord
GET /api/v1/userCaptionRemoval/detail?_id={_id}
DELETE /api/v1/userCaptionRemoval/{_id}
```

---

## 13. Virtual Try-On

### Start Virtual Try-On
```
POST /api/v1/virtualTryOn/start
Body: { name, image_urls: [person_url, person_mask_url, clothing_url, clothing_mask_url] }
Exactly 4 URLs in order!
```

### List/Detail/Delete
```
GET /api/v1/virtualTryOn/allRecords?pageNum=1&pageSize=10
GET /api/v1/virtualTryOn/{_id}
DELETE /api/v1/virtualTryOn/{_id}
```

---

## 14. Background Matting & Replacement

### List Background Images
```
GET /api/v1/anchor/background_list
```

### Add Custom Background
```
POST /api/v1/anchor/add_background
Body: { image_url }
```

### Delete Custom Background
```
DELETE /api/v1/anchor/background/{_id}
```

---

## 15. Product Avatar

### Start Product Avatar
```
POST /api/v1/productAvatar/start
```

---

## 16. Miscellaneous

### Get Remaining Credits/Coins
```
GET /api/v1/user/remainingCoins
Response: { data: { coins: 2836 } }
```

### List Available Languages
```
GET /api/v1/anchor/language_list?lang=en
```

### Save URL to A2E Storage
```
POST /api/v1/tos/transferToStorage
Body: { url }
Use for unstable external URLs before passing to other endpoints.
```

### Add Watermark
```
POST /api/v1/watermark/add
```

### Get R2 Upload Presigned URL
```
GET /api/v1/tos/getPresignedUrl
For direct file uploads to A2E storage.
```

---

## Common Patterns

All async tasks follow the same pattern:
1. `POST .../start` → get `_id` + `current_status: "initialized"`
2. Poll `GET .../{_id}` or `GET .../allRecords` until `current_status: "completed"`
3. Result URLs in response (image_urls, result_url, video_url etc.)
4. Status values: `initialized` → `processing` → `completed` | `failed`
5. On failure: check `failed_message` + `failed_code`
6. Result URLs are signed and expire after ~3 days

---

## 17. Kling 3.0 (Video Generation)

Cinema-grade video from text or image. Available at https://video.a2e.ai/kling-video-3.0

### Modes
- **Text** — Generate video from text prompt
- **Image** — Upload reference image → animate
- **Motion Control** — Transfer motion from reference video onto image

### Features
- Sound generation (built-in audio)
- Creativity control (higher = more creative)
- End frame guide (specify ending scene)
- Quality: STD / HD
- Duration: 5s / 10s

### API (likely same pattern)
```
POST /api/v1/userKling/start (unconfirmed endpoint name)
```

---

## 18. Wan 2.6 (Video Generation)

Cinematic videos with synced audio. Available at https://video.a2e.ai/wan-2-6

---

## 19. Sora 2 Pro (OpenAI Video)

OpenAI's video model via a2e. Available on the platform.

---

## 20. Seedance 1.5 Pro

Multi-shot high-quality video generation.

---

## 21. Veo 3.1 (Google Video)

Next-gen video creation powered by Google.

---

## 22. GPT Image 1.5

True-color precision rendering (OpenAI image model).

---

## 23. Flux 2 Pro

Speed-optimized detail generation (Black Forest Labs).

---

## 24. Grok Imagine

xAI's Grok text/image to video.

---

## 25. Photobook

Generate multiple portraits from one photo. Highly relevant for AI Photoshooting (DAN-102)!

---

## 26. Head Swap

Seamless head replacement technology. Different from Face Swap — replaces entire head, not just face.

```
Upload: Head Image (frontal, single-person) + Source Video/Image
```

---

## 27. Image Editor

AI-powered image editing tools.

---

## 28. Nano Banana 2

Next-gen image generation model (newer than Nano Banana Pro).

---

## All Products on a2e.ai (as of March 2026)

| Product | Category | API Available | Notes |
|---|---|---|---|
| Text to Image (A2E) | Image Gen | ✅ | General + Manga styles |
| Nano Banana Pro | Image Gen | ✅ | Gemini-2.5-Flash |
| Nano Banana 2 | Image Gen | Likely ✅ | Newer model |
| GPT Image 1.5 | Image Gen | TBD | OpenAI model |
| Flux 2 Pro | Image Gen | TBD | Black Forest Labs |
| Grok Imagine | Image Gen | TBD | xAI |
| Face Swap | Face | ✅ | Photos + Videos |
| Head Swap | Face | ✅ | Full head replacement |
| Image to Video | Video Gen | ✅ | 5s 720p, face-optimized |
| Video to Video | Video Gen | ✅ | Motion transfer |
| Kling 3.0 | Video Gen | ✅ | Text/Image/Motion modes |
| Wan 2.6 | Video Gen | TBD | Cinematic + audio |
| Sora 2 Pro | Video Gen | TBD | OpenAI |
| Seedance 1.5 Pro | Video Gen | TBD | Multi-shot |
| Veo 3.1 | Video Gen | TBD | Google |
| AI Avatar | Avatar | ✅ | Lip-sync videos |
| Talking Photo | Avatar | ✅ | Animate photos |
| Talking Video | Avatar | ✅ | Animate videos |
| Photobook | Portrait | TBD | Multiple portraits from 1 photo |
| Image Editor | Editing | TBD | AI editing tools |
| Virtual Try-On | Fashion | ✅ | Clothing swap |
| AI Dubbing | Audio | ✅ | Language conversion + voice clone |
| Caption Removal | Video Edit | ✅ | OCR + inpainting |
| TTS + Voice Clone | Audio | ✅ | Azure + ElevenLabs + custom |
| Background Replace | Editing | ✅ | Avatar backgrounds |
| Product Avatar | Marketing | ✅ | Product presentations |

## Known Quirks
- NanoBanana GET by ID returns 404 — use allRecords to find tasks
- Text2Image input_images parameter does NOT work — use NanoBanana for reference images
- German text in Text2Image often has typos — NanoBanana (Gemini) handles it correctly
- Many newer models (Kling, Wan, Sora, Veo, Flux, Grok) likely have API endpoints but docs not yet in llms.txt
- Some pages require auth to view (redirect to sign-in)
- Product URLs vary: some at /video-generator/X, others at /X or /X-Y-Z
