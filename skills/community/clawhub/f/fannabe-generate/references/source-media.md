# Source media: image-to-video, edits, motion control, character swap

Many workflows attach existing media to an AI's input slots via repeatable `--source inputKey=mediaId`. Discover the slots with `fannabe ai schema <aiId>` (the "Source media" section lists each slot's inputKey).

## Two id kinds, never interchangeable

- **Content id** (the `ID` column): downloads and video tools (`content download`, `caption-on-video`).
- **Media id** (the `Media ID (--source)` column, or an upload's `imageId`/`videoId`/`audioId`): `--source` slots on generation.

```bash
fannabe models gallery <modelId> --media-type image       # shows both id columns
fannabe uploads image ./scene.png                             # prints contentId AND imageId
```

## Image-to-video

```bash
fannabe generate create seedance-1-5-pro \
  --model <modelId> --media-type video --concept-type video-from-image \
  --source image-1=<mediaId> \
  --prompt "she sips her coffee and smiles" \
  --set duration=5 --set resolution=720p \
  --wait --wait-timeout 15m --download ./output
```

## Motion control (transfer a clip's movement onto a model still)

```bash
fannabe generate create kling-2-6-motion-control \
  --model <modelId> --media-type video \
  --source video-1=<motionVideoMediaId> \
  --source image-1=<modelImageMediaId> \
  --set resolution=1080p --set keepOriginalSound=true \
  --wait --wait-timeout 15m --download ./output
```

Output length follows the motion clip (3-30s) and cost is priced per second. Need a model still that matches the clip's framing? `fannabe video frame <videoContentIdOrFile> --time 1.5 --upload` extracts a frame and returns an `imageId` ready for `image-1`.

## Character swap

The `character-ref` slot is auto-filled from the model's stored default swap image; the scene-ref must be an account-level uploaded image (`fannabe uploads image ...`, then its `imageId`). Read `ai schema <swapAiId>` for the exact slot keys.
