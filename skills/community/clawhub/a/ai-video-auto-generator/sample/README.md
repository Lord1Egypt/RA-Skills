# Sample: Quick Experience Video

A minimal 5-shot short video script for testing the pipeline.

## Quick Start

```bash
# 0. Quick demo (30 seconds, no API key needed)
#    在 skill 根目录执行
python skills/project-generate/scripts/pipeline.py --project sample --mode demo

# 1. Setup environment (auto-install missing deps)
#    在 skill 根目录执行
python skills/project-generate/scripts/pipeline.py --project sample --mode setup

# 2. Run the full pipeline
#    在 skill 根目录执行
python skills/project-generate/scripts/pipeline.py --project sample --mode auto
```

## What It Does

This sample contains a 15-second drama scene:
- 1 character (小墨)
- 1 scene (天台 rooftop)
- 5 shots with camera movement variety (dolly-in, closeup, tilt-up, static, wide)
- Emotional arc: calm → reflective → tense → resolved

## Notes

- Requires Agnes AI API Key (`~/.agnes-api-key` or configured in `script.json`)
- First run will auto-install Python dependencies (opencv, edge-tts, etc.)
- The auto pipeline will validate and auto-fix the script's narrative structure
