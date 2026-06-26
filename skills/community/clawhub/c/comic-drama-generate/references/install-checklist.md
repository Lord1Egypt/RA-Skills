# Install checklist

This skill depends on these installed skills:

- `video-prompt-generator`
- `nano-banana-pro`
- `sora-2-generate`

## Example install commands

```bash
npx clawhub@latest install video-prompt-generator
npx clawhub@latest install nano-banana-pro
npx clawhub@latest install sora-2-generate
```

## Before producing an episode

Verify:
- the prerequisite skill folders exist
- required API credentials are configured for the prerequisite skills
- `ffmpeg` is installed locally
- there is enough API credit for script, image, and video generation
- the workflow will pass public URLs, not local files, between image and video steps

## API key handling note

This skill does not define a separate API key of its own.

In most setups, the prerequisite skills are configured with:

- `NANOPHOTO_API_KEY`

Preferred execution order:

1. Use the prerequisite skills through their normal skill execution path and rely on their configured env.
2. If direct script execution is necessary, preserve the same contract by ensuring `NANOPHOTO_API_KEY` is available in the shell.
3. If the shell cannot inherit that env, use `--api-key <KEY>` as an explicit fallback.
4. Only use direct config-file reads as a debugging or recovery technique, not as the default workflow.

Example shell-first pattern:

```bash
export NANOPHOTO_API_KEY="your_key_here"

python3 skills/nano-banana-pro/scripts/nano_banana_generate.py \
  --prompt "..." \
  --mode generate \
  --aspect-ratio 9:16 \
  --image-quality 2K
```

Fallback pattern:

```bash
python3 skills/nano-banana-pro/scripts/nano_banana_generate.py \
  --api-key "$NANOPHOTO_API_KEY" \
  --prompt "..." \
  --mode generate \
  --aspect-ratio 9:16 \
  --image-quality 2K
```
