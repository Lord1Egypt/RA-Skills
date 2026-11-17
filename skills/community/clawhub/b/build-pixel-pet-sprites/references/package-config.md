# Package configuration

Pass a JSON configuration to `scripts/build_sprite_package.py` after removing the
chroma-key background.

```json
{
  "character": "assistant-pet",
  "atlas_name": "assistant-pet-atlas.png",
  "frame": { "width": 256, "height": 256 },
  "actions": [
    {
      "name": "idle",
      "frame_count": 6,
      "frame_duration_ms": 120,
      "loop": true,
      "anchor": { "x": 0.5, "y": 0.92 }
    },
    {
      "name": "success",
      "frame_count": 6,
      "frame_duration_ms": 100,
      "loop": false,
      "anchor": { "x": 0.5, "y": 0.92 }
    }
  ]
}
```

The source atlas rows must match the action order. The script resizes the complete atlas
with nearest-neighbor sampling to `max(frame_count) * frame.width` by
`len(actions) * frame.height`, then writes:

- `atlas/`
- `strips/`
- `frames/`
- `preview/`
- `sprite-manifest.json`
- a ZIP sibling

Commands:

```powershell
python scripts/build_sprite_package.py transparent-atlas.png package-config.json output/pet
python scripts/align_sprite_frames.py output/pet output/pet-aligned
python scripts/validate_sprite_package.py output/pet-aligned
```

Use the aligned package for delivery and web integration. The manifest records action
rows, frame counts, durations, loop flags, anchors, paths, and alignment offsets.
