# Video Prompt Guide

## Prompt Structure

A strong text-to-video prompt usually follows this order:

```
[subject] + [action] + [camera movement] + [scene details] + [lighting] + [style]
```

Example:

```
A white sports car drifting through a rainy Tokyo intersection, low-angle tracking shot,
wet asphalt reflections, neon signs, cinematic night lighting, realistic film look
```

## Aspect Ratio Guidance

- `16:9`: landscape scenes, cinematic shots, desktop playback
- `9:16`: shorts/reels/tiktok style vertical videos
- `1:1`: square social feed placements

## Prompt Tips

1. Use explicit camera language: `tracking shot`, `slow push-in`, `aerial pull-back`.
2. Describe motion clearly: `walks slowly`, `turns toward camera`, `water splashes`.
3. Include lighting and mood: `golden hour`, `soft studio`, `dramatic backlight`.
4. Keep one core scene per prompt to avoid chaotic results.
5. If retrying the same prompt, use a new `idempotency_key` for a fresh generation.

## Ready-to-Use Examples

### Cinematic Landscape (`16:9`)

```
An aerial shot of snow mountains at sunrise, slow forward drone movement,
mist in the valleys, warm orange rim light, ultra realistic cinematic style
```

### Vertical Lifestyle (`9:16`)

```
A skateboarder jumping over a stair set, handheld follow camera,
urban street textures, afternoon sunlight, energetic documentary style
```

### Product Motion (`1:1`)

```
A luxury perfume bottle rotating on black glass, macro close-up camera move,
water droplets, controlled studio highlights, premium ad style
```
