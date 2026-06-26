---
name: video-watermark-remover
description: Remove watermarks from videos using ffmpeg delogo filter. Use this skill whenever the user wants to remove a watermark from a video, asks to remove a logo/text overlay, sends a video with visible watermarks, or says "去除水印" / "remove watermark" / "去水印". Works for both fixed-position and dynamically-moving watermarks (segmented delogo approach). Does NOT remove transparent/AI-generated complex watermarks that require inpainting — those need a different pipeline.
---

# Video Watermark Remover

Remove watermark/logo/text overlays from videos using ffmpeg's `delogo` filter.

## Core Logic

**Step 1: Extract sample frames**
Extract frames at 1-second intervals to locate watermark positions:
```bash
for t in 1 2 3 4 5; do
  ffmpeg -y -ss 00:00:0$t -i "$INPUT" -frames:v 1 "/tmp/wm_frame_$t.jpg" 2>/dev/null
done
```

**Step 2: Analyze with vision model**
Use the `image` tool to analyze the sample frames. Ask for:
- Exact watermark positions (which corner/edge)
- Pixel bounding box: x, y, width, height for a WxH resolution video
- Whether watermarks are in the same position across all frames (fixed) or move (dynamic)

**Step 3: Build segmentation strategy**

*Fixed watermark* (same position throughout):
- One delogo pass on entire video

*Dynamic watermark* (position changes at specific times):
- Identify segment boundaries (e.g., 0-3.5s bottom-right, 3.5s+ left edge)
- Process each segment separately with its own delogo coordinates
- Concatenate segments back together

**Step 4: Process and verify**
```bash
# Single segment
ffmpeg -y -i "$INPUT" -vf "delogo=x=$X:y=$Y:w=$W:h=$H" -c:a copy "$OUTPUT"

# Multiple segments
# Process each segment separately with -ss/-t, then concat
```

Verify each segment's result with the vision model before final delivery.

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `x, y` | Top-left corner of watermark region |
| `w, h` | Width and height of watermark region |
| `INPUT` | Input video path |
| `OUTPUT` | Output video path |

**Finding exact coordinates:**
- Vision model gives normalized coordinates on 0-1000 scale — convert to actual pixels
- For a 720x1280 video: `actual_x = normalized_x * width / 1000`
- Always add 5-10px padding to the detected region to ensure full coverage

## Dynamic Watermark Segmentation

When watermark moves between distinct positions:

1. **Identify transition points** — Note which frames have watermarks at which positions
2. **Create segments** — Each position change = new segment boundary
3. **Process each segment** — Apply correct delogo coordinates to each time range
4. **Concatenate** — Use ffmpeg concat with a manifest file:
   ```
   file 'seg1.mp4'
   file 'seg2.mp4'
   ```
   ```bash
   ffmpeg -y -f concat -safe 0 -i concat.txt -c copy output.mp4
   ```

**Example segmentation:**
| Segment | Time Range | Watermark Position |
|---------|-----------|-------------------|
| 1 | 0-3.5s | Bottom-right (x=540,y=1195,w=165,h=55) |
| 2 | 3.5-5s | Left edge (x=30,y=480,w=160,h=210) |

## Handling Multiple Watermarks

If multiple watermarks exist simultaneously (e.g., corner logo + username handle):
- Identify which the user wants removed vs. preserved
- Apply multiple `delogo` filters in the same vf string:
  ```bash
  -vf "delogo=x=540:y=1195:w=165:h=55,delogo=x=30:y=480:w=160:h=210"
  ```

## Output Delivery

- Save to `/root/.openclaw/workspace/downloads/`
- Send via `message` tool with `media` parameter
- Confirm with user before final delivery

## Limitations

- `delogo` fills the region with a blurred/averaged patch — works best on simple/static backgrounds
- Semi-transparent watermarks, complex AI-generated watermarks, and moving watermarks over textured backgrounds may still show traces
- For AI inpainting (natural content-aware fill): this skill cannot do it — inform the user and suggest inpainting pipeline if delogo result is unsatisfactory
