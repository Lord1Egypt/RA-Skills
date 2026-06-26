# chaoji-skills

Agent skill library for ChaoJi OpenAPI — enables AI agents (Claude Code, Cursor, OpenClaw, etc.) to perform virtual try-on, image generation, cutout, and more through purpose-built, scene-specific workflows.

## Security

**Important:** This skill requires API credentials. The runner does not auto-install packages; runtime repair is manual.

See [SECURITY.md](SECURITY.md) for:
- Credential handling details
- Permission requirements
- Security audit checklist

## Layout

- Root entry skill: `SKILL.md` (global routing guidance)
- Tool aggregate skill: `chaoji-tools/`
- Scene skills: `skills/` (`chaoji-tryon`, `chaoji-tryon-fast`, `chaoji-tryon-shoes`, `chaoji-img2img`, `chaoji-cutout`)

## Quick Start

1. Install skills

```bash
clawhub install chaoji-skills
```

2. Configure credentials

- `CHAOJI_AK` + `CHAOJI_SK` (env), or
- `~/.chaoji/credentials.json`

```json
{
  "access_key": "your_access_key",
  "secret_key": "your_secret_key"
}
```

3. Smoke test

```bash
python chaoji-tools/scripts/run_command.py \
  --command remaining_quantity_of_beans \
  --input-json '{}'
```

Expected output:

```json
{
  "ok": true,
  "command": "remaining_quantity_of_beans",
  "result": {
    "code": 2000,
    "data": { "remaining_quantity": 12345 }
  }
}
```

4. Sensitive data self-check (before commit/push/package)

```bash
rg -n --hidden -S \
  -g '!.git' -g '!node_modules' -g '!__pycache__' \
  '(CHAOJI_AK|CHAOJI_SK|access_key|secret_key|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9_-]{20,}|BEGIN (RSA|EC|OPENSSH) PRIVATE KEY)' .
```

- Run this before `git commit`, `git push`, and any zip/tar delivery.
- No output means no obvious plaintext secret was found by this rule set.

## Skills

### chaoji-tryon

Real-person virtual try-on (human try-on). Upload a garment image and a model photo to generate high-quality try-on results. Supports upper, lower, and full-body garments.

Triggers: 真人试衣, 模特换装, 换装, human tryon

---

### chaoji-tryon-fast

Quick virtual try-on preview. Faster processing, suitable for rapid iteration and preview before committing to full-quality generation.

Triggers: 快速试衣, quick tryon

---

### chaoji-tryon-shoes

Shoe try-on. Upload 1-3 shoe product images and a model photo to generate shoe try-on results. Multiple shoe angles improve quality.

Triggers: 试鞋, 鞋靴试穿, shoes tryon

---

### chaoji-img2img

Image-to-image generation. Generate new images from reference images + text prompts. Supports up to 14 reference images. Suitable for e-commerce material generation, style transfer, and creative design.

Triggers: 图生图, 素材生成, 潮绘, image to image

---

### chaoji-cutout

Intelligent image cutout / segmentation. Supports portrait, clothing, pattern, and general segmentation with auto-detection mode. Sync API — instant results.

Triggers: 抠图, 去背景, 分割, cutout, segmentation
