# Agnes Video Generator

A skill for generating AI videos using Agnes-Video-V2.0 model.

## Capabilities

- Text-to-video generation
- Image-to-video animation
- Multi-image and keyframe animation (requires script extension)
- Asynchronous task handling with auto-polling
- Returns direct video URL

## Usage

The skill is invoked automatically when the user requests video generation. It accepts:

- `prompt` (string, required): Video description
- `image` (string, optional): Source image URL for img2vid
- `num_frames` (number, optional): Frame count, must be 8n+1 (e.g., 81, 121, 241, 441)
- `frame_rate` (number, optional): FPS, default 24
- `size` (string, optional): Resolution like "1152x768"
- `seed` (number, optional): Random seed
- `negative_prompt` (string, optional): What to avoid
- `extra_mode` (string, optional): e.g., "keyframes" for multi-image

## Implementation

- Endpoint: `https://apihub.agnes-ai.com/v1/videos`
- Query: `GET https://apihub.agnes-ai.com/agnesapi?video_id=...`
- Authentication: Bearer token from `AGNES_API_KEY` environment variable
- Model: `agnes-video-v2.0`
- Polls every 5 seconds (up to ~10 minutes) until completion

## Notes

- Video generation is asynchronous; script handles polling automatically.
- `remixed_from_video_id` field in the final response holds the video URL.
- Pricing: $0.005 per second (check Agnes docs for current rates).

## Example

```bash
node generate.js --prompt "A cinematic shot of a cat walking on the beach at sunset" --num_frames 121 --frame_rate 24 --size 1152x768
```
