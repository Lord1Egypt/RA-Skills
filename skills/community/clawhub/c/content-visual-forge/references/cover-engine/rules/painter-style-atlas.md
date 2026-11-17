# Painter Style Atlas

## Purpose

Use painter-style atlas data as local style metadata for calibration, not as live-query dependencies or artist-imitation directives.

## Runtime Data

Default runtime must use the local snapshot:

- `assets/style-atlas/qiaomu-style-atlas.snapshot.json`

The snapshot source is:

- Qiaomu Artist Style: `https://style.qiaomu.ai/`

Snapshot date: 2026-05-20. The local snapshot contains 383 metadata entries across 12 style families. It stores names, broad movement labels, cues, and source image paths only; it does not vendor generated images.

Do not query the external website during normal generation. Refresh the snapshot only as a maintenance action with:

```bash
python content-visual-forge/scripts/style-atlas/fetch_qiaomu_style_atlas.py --snapshot-date YYYY-MM-DD
```

## When To Use

Use this rule when:

- a user asks for a more specific painterly, illustrator, cinematic, or art-historical direction
- `cover-card` needs more precise style routing than broad labels such as `painterly_mood`
- `wechat-inline-image` needs an atmosphere family for low-text reading-rhythm images
- a prompt package needs style alternatives for exploration

Do not use it when:

- the output is a text-heavy card that should be engineered through layout templates
- the requested style is irrelevant to the source content
- the user is asking to copy a specific artwork, image, composition, or living artist's distinctive style

## Translation Protocol

First load the local snapshot, then select a style family or entry that fits the current content. Never pass an atlas entry through as plain `in the style of {artist}` by default. Convert the reference into controllable visual factors:

1. movement or broad tradition
2. line quality
3. color temperature and palette contrast
4. light behavior
5. spatial depth and composition logic
6. texture or medium
7. emotional register
8. typography compatibility and blank-space needs

Then combine those factors with the current article topic, output mode, and execution mode.

## Output Fields

When this rule is used, `style_routing` should add:

- `atlas_snapshot`: local snapshot path and snapshot date
- `style_atlas_status`: `loaded`, `unavailable`, `rejected`, or `not_applicable`
- `atlas_reference`: local entry id, family id, or user-provided atlas entry
- `atlas_family`: broad movement or style family
- `style_factors`: 4-8 translated visual factors
- `artist_name_policy`: `none`, `public_domain_allowed`, or `avoid_artist_name`
- `prompt_style_phrase`: model-safe style phrase using movement and visual factors
- `blocked_mimicry`: artist names, artworks, layouts, or recognizable signatures that must not be copied

## Safe Prompt Pattern

Prefer:

```text
Use a restrained impressionist-inspired atmosphere: soft broken light, visible brush texture, airy color transitions, low-contrast natural palette, generous blank space for later title overlay.
```

Avoid:

```text
Make it exactly like [artist], copying their signature composition, brushwork, and recognizable motifs.
```

## Atlas Family Mapping

- Emotional essay: impressionist atmosphere, cinematic window light, subdued classical chiaroscuro, soft surreal space.
- Culture / history: classical composition, Oriental line-and-blank-space logic, archival book-cover restraint.
- AI beginner / science: warm illustrated learning map, architectural spatial order, gentle retro-futurist concept art.
- Business analysis: modern poster, geometric abstraction, editorial minimalism, restrained pop-art contrast.
- Lifestyle: golden-age illustration warmth, watercolor editorial illustration, light cinematic photography.
- Speculative / technology: concept-design depth, controlled cyberpunk accents, abstract machine-space metaphors.

## Safety Notes

- Public-domain artist names may be used as optional internal reference anchors, but production prompts should still prefer style factors and movements.
- Avoid direct imitation of living or recently active artists, photographers, designers, manga artists, film directors, or recognizable IP universes.
- Do not use atlas images as layout references unless the user supplies explicit rights and asks for layout study; even then, transform composition and decorative systems.
- Do not treat `image_path` values in the snapshot as local assets. They are source paths for optional human inspection, not production inputs.

## Failure Contract

| 状态 | 触发条件 | 动作 |
|---|---|---|
| `loaded` | 本地 snapshot 存在、可读、与任务相关 | 使用风格因子进入 Prompt / Render Package |
| `unavailable` | snapshot 缺失、JSON 损坏或读取失败 | 不查询外部网站；改用模板族默认风格，记录风险 |
| `rejected` | 用户要求复制特定画家、名作、IP、构图或在版权上高风险 | 拒绝仿写请求，转译为宽风格家族或要求用户换方向 |
| `not_applicable` | 当前任务不需要图鉴风格或是文字密集工程渲染 | 不加载图鉴，不把图鉴元素塞入提示词 |
