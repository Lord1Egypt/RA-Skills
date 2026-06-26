---
name: best-practice-skill-creator
description: Create OpenClaw skills from best practice videos or image sequences. Use when creating skill from video, generating skill from screenshots, converting tutorial to skill, building best practice automation.
user-invocable: true
metadata: {"openclaw":{"emoji":"🎓","requires":{"anyBins":["python3","python"]},"os":["darwin","linux","win32"],"primaryEnv":"MLLM_API_KEY"}}
---

# Best Practice Skill Creator

You are a skill that creates OpenClaw-compatible skills from best practice demonstrations.

## What You Do

You accept:
1. **Video files** (mp4, mov, avi, webm) showing a best practice workflow
2. **Image sequences** (png, jpg, webp) capturing step-by-step screenshots
3. **Text description** explaining what the task accomplishes and any context

You then use a Multimodal LLM (GPT-5.4 or Gemini 3.1 Pro Preview) to:
- Analyze the visual content frame by frame
- Extract the step-by-step procedure
- Identify tools, commands, and patterns used
- Generate a complete OpenClaw-compatible skill

## Usage

```bash
# From video + description
python3 best_practice_skill_creator/main.py \
  --input video.mp4 \
  --description "How to set up a CI/CD pipeline with GitHub Actions" \
  --output ./skills/ci-cd-setup

# From image sequence + description
python3 best_practice_skill_creator/main.py \
  --input ./screenshots/ \
  --description "How to configure Kubernetes rolling deployments" \
  --output ./skills/k8s-rolling-deploy

# Specify provider
python3 best_practice_skill_creator/main.py \
  --input video.mp4 \
  --description "Task description" \
  --provider openai \
  --output ./skills/my-skill
```

## Configuration

Edit `best_practice_skill_creator/config.yaml` to set your MLLM provider, API key, and model.

Environment variables override config file values:
- `MLLM_PROVIDER` — `openai` or `gemini`
- `MLLM_API_KEY` — Your API key
- `MLLM_BASE_URL` — Custom API endpoint
- `MLLM_MODEL` — Model identifier

## Output

The generated skill directory contains:
- `SKILL.md` — A fully compliant OpenClaw skill with proper frontmatter
- Ready for `clawhub publish` or direct use in `~/.openclaw/skills/`
