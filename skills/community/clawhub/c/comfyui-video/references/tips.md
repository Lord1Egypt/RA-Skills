# Tips & Best Practices

## Model Selection

| Version | Size | GPU Compat | Recommended |
|---------|------|------------|-------------|
| dev (bf16) | 43GB | All (Turing+) | ✅ Yes |
| Kijai fp8 | 22GB | Ampere+ only | ⚠️ Not for Turing |
| distilled + LoRA | +7.1GB | All | ✅ Essential |

## Prompt Engineering for I2V

### Do's
```
"Extreme close-up of a single human eye, the pupil reflecting a neon city 
skyline with flickering lights, tears welling up, water droplets on eyelashes, 
hyper-realistic detail, macro lens, cinematic lighting, 8k"
```

### Don'ts
```
"a girl crying in the rain"
```

### Key Elements
- **Specific actions** > vague descriptions
- **Environment**: rainy, neon, cinematic, moody
- **Camera**: close-up, wide shot, tracking shot, macro lens
- **Quality**: 8k, ultra detailed, photorealistic, film grain

## Reference Image Selection

1. **Clear composition** — Subject should be prominent
2. **Style consistency** — Reference style transfers to video
3. **Character consistency** — Use same image for all scenes in a series

## Time Estimation

```
Total Time = per_step × steps × scenes

Examples:
  221s × 15 × 7 = 434 min ≈ 7.2 hours
  221s × 25 × 7 = 726 min ≈ 12.1 hours
```

## VRAM Management

| Phase | Usage |
|-------|-------|
| Model loaded | ~40GB |
| Sampling | ~40GB |
| VAE decode | ~28GB |
| Idle | ~9GB |

### Avoid OOM
1. Don't run multiple generations in parallel
2. Complete one before starting next
3. Restart ComfyUI if OOM occurs

## Video Post-Processing

### Concatenate Scenes
```bash
echo "file 'scene1.mp4'" > list.txt
echo "file 'scene2.mp4'" >> list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Extract Frames
```bash
ffmpeg -i input.mp4 -vf "fps=1" frame_%04d.png  # 1 frame/sec
```

## Speed Optimization

| Method | Effect | Trade-off |
|--------|--------|-----------|
| Reduce steps 25→15 | -40% time | Minimal quality loss |
| Lower frames 121→72 | Shorter clip | Doesn't reduce time |
| Distilled LoRA | Faster convergence | **Must install** |
| Lower resolution | Significant speedup | For testing only |

**Remember**: Frame count does NOT affect generation time.
