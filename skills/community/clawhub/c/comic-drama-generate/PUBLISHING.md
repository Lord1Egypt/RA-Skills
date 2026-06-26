# Publishing / provenance notes

- Publisher: NanoPhotoHQ
- Service homepage: https://nanophoto.ai
- API key management page: https://nanophoto.ai/settings/apikeys
- Skill purpose: generate serialized comic-drama / 漫剧 episodes through a character-consistent multi-skill workflow using script generation, three-view sheets, keyframes, image-to-video clips, and local ffmpeg editing.

## Required credential

This skill itself does not require a new credential beyond the credentials required by its prerequisite skills.

Prerequisite skills may require:

- `NANOPHOTO_API_KEY` — required for NanoPhoto-backed prerequisite skills such as `video-prompt-generator`, `nano-banana-pro`, and `sora-2-generate`

Do not paste API keys into chat. Configure them through the platform's secure environment-variable settings for the prerequisite skills.

## API key execution note

When an agent uses prerequisite skills through normal skill execution, it should rely on the prerequisite skill env configuration.

When an agent directly runs bundled helper scripts through `exec`, it should preserve the same environment-variable contract first, typically by ensuring `NANOPHOTO_API_KEY` is available in the shell. Use `--api-key` only as a fallback when shell env inheritance is unavailable. Do not treat direct config-file reads as the normal workflow.

## Prerequisite skills

Install these skills before using this skill:

- `video-prompt-generator`
- `nano-banana-pro`
- `sora-2-generate`

Example install pattern:

```bash
npx clawhub@latest install video-prompt-generator
npx clawhub@latest install nano-banana-pro
npx clawhub@latest install sora-2-generate
```

## Safety / usage notes

- Only generate scripts, images, and videos you are authorized to create or process.
- For image-driven steps, only use public image URLs you are comfortable sending to the underlying generation services.
- Do not provide private or sensitive images as public URLs.
- This skill orchestrates other skills and local ffmpeg editing; it does not ask for unrelated credentials.
