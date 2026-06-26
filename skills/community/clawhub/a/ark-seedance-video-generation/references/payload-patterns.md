# Payload Patterns

Use this file when the request needs advanced Ark request bodies that are more precise than the exposed CLI flags.

Write one of these patterns to a JSON file in the workspace, then execute the existing script with `--payload-file`.

Do not build another script to send these payloads.

## Pattern 1: Basic Text-To-Video

```json
{
  "model": "<MODEL_ID>",
  "content": [
    {
      "type": "text",
      "text": "A cinematic rainy alley at night, slow camera push, neon reflections, realistic lighting"
    }
  ],
  "resolution": "1080p",
  "ratio": "16:9",
  "duration": 5,
  "watermark": true
}
```

## Pattern 2: Image-To-Video With Tail Frame

```json
{
  "model": "<MODEL_ID>",
  "content": [
    {
      "type": "text",
      "text": "Subtle blink, slight hair movement, stable framing, natural motion"
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "data:image/png;base64,<BASE64_IMAGE>"
      }
    }
  ],
  "ratio": "9:16",
  "duration": 5,
  "return_last_frame": true
}
```

## Pattern 3: Multi-Input With Audio

```json
{
  "model": "<MODEL_ID>",
  "content": [
    {
      "type": "text",
      "text": "Use the image as the opening frame and use the audio as the background soundtrack."
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "https://example.com/input.png"
      }
    },
    {
      "type": "audio_url",
      "audio_url": {
        "url": "https://example.com/music.mp3"
      }
    }
  ],
  "resolution": "720p",
  "duration": 5
}
```

## Pattern 4: Draft Task Reuse

```json
{
  "model": "<MODEL_ID>",
  "content": [
    {
      "type": "draft_task",
      "draft_task": {
        "id": "cgt-xxxxxxxx"
      }
    }
  ]
}
```

## Pattern 5: Seeded Repro Attempt

```json
{
  "model": "<MODEL_ID>",
  "content": [
    {
      "type": "text",
      "text": "Luxury perfume ad, glossy studio set, slow orbit camera, premium lighting"
    }
  ],
  "resolution": "1080p",
  "ratio": "16:9",
  "duration": 5,
  "seed": 42,
  "camera_fixed": false,
  "watermark": true
}
```

## Pattern 6: Asset ID Input

```json
{
  "model": "<MODEL_ID>",
  "content": [
    {
      "type": "text",
      "text": "Create a short promo clip from the provided asset."
    },
    {
      "type": "image_url",
      "image_url": {
        "url": "asset://<ASSET_ID>"
      }
    }
  ],
  "duration": 5
}
```

## Usage Rule

After writing a payload file, run the bundled script with:

```powershell
node "./scripts/seedance-video.js" --payload-file "<payload.json>" --download-dir "<dir>"
```

Keep `request.json`, `task.json`, and downloaded assets together in one output folder for reproducibility.
