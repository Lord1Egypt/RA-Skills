# IMAGE PROMPT CREATION

> **Component** | Specific to create-image-prompt workflow
> Full lifecycle: read dependencies → scope → execute → validate → deliver.

---

> **PREREQUISITES**
>
> - Workspace-independent workflow (no workspace state update)
> - Output language: Always English (required for AI image models)

---

## STEP 1: READ DEPENDENCIES

- Read `objectives.md` — understand MISSION, OBJECTIVES, phased approach
- Read `template.md` — output structure, copy-paste ready format
- Read `image-prompt-engineering.md` — core guide for this workflow
- Scan `styles/` folder for available style definitions (optional)

---

## STEP 2: SCOPE CLARIFICATION

Guide: `./references/guides/image-prompt-engineering.md`

Gather complete information for effective AI image prompts.

### Required Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `subject` | Main subject or concept | "A cyberpunk city at night with neon lights" |
| `style` | Visual style (from library or custom) | "voxel-art", "photorealistic", "anime" |
| `purpose` | Use case | "Blog header", "Social media post" |

### Optional Parameters (smart defaults)

| Parameter | Default |
|-----------|---------|
| `target_model` | All 4 (Universal, ChatGPT, Gemini, Grok) |
| `aspect_ratio` | Infer from purpose |
| `camera_angle` | Eye-level |
| `framing` | Infer from subject |
| `negative_space` | Infer from purpose |
| `mood` | Infer from subject/style |
| `color_palette` | Follow style guidelines |
| `lighting` | Style-appropriate |
| `number_of_variants` | 1 |

### Clarification Path

**Fast** (clear subject + style + purpose, experienced user): Confirm understanding → proceed.

**Selective** (partial info, 1-3 gaps): Ask targeted questions about unclear aspects only.

**Full** (vague request, unsure user): Guide through all key parameters systematically.

### Confirm Requirements

```
Subject: {subject}
Style: {style_name}
Purpose: {purpose}
Target Models: {models}
Aspect Ratio: {aspect_ratio}
Camera Angle: {camera_angle}
Framing: {framing}
Mood: {mood}
Variants: {number_of_variants}

Proceed? (Y/modify): ___
```

---

## STEP 3: EXECUTION

Guide: `./references/guides/image-prompt-engineering.md`

### Phase 1: Style & Composition Planning

1. Internalize style rules from style definition or custom description
2. Plan composition layout (camera angle, framing, depth layers)
3. Establish focal point and visual flow
4. Plan negative space handling if required

### Phase 2: Prompt Construction

Build layered prompts:

| Layer | Content |
|-------|---------|
| **Subject** | Main subject with key details |
| **Style** | Visual style characteristics |
| **Composition** | Camera, framing, perspective |
| **Environment** | Setting, background, context |
| **Lighting** | Light source, quality, direction |
| **Mood** | Atmosphere, emotion, feeling |
| **Technical** | Quality markers, rendering style |

### Phase 3: Model Optimization

Adapt prompts for each target model:

- **Universal (Midjourney/SD):** Prompt text + inline parameters (`--ar`, `--q`)
- **ChatGPT Image (DALL·E 3):** Natural language, separate Size/Quality/Style settings
- **Gemini Image (Imagen 3):** Natural language, Aspect Ratio + Safety Filter settings
- **Grok Image (Flux):** Detailed descriptive prompt, Aspect Ratio + Guidance + Steps settings

### Phase 4: Variant Generation (conditional)

> Only if `number_of_variants > 1`

Create controlled variations maintaining style consistency. Strategies: composition, mood, lighting, color, time of day. Each variant gets all model-optimized prompts.

---

## STEP 4: VALIDATION

- [ ] Mission and objectives achieved
- [ ] Subject clearly described
- [ ] Style consistency maintained
- [ ] Composition well-designed with focal point
- [ ] Prompts optimized for all target models with correct syntax
- [ ] Each prompt copy-paste ready with zero editing needed
- [ ] Settings clearly displayed per model
- [ ] VALIDATION CRITERIA from objectives.md completed

**If fails:** Return to Step 3. **If passes:** Proceed to Step 5.

---

## STEP 5: DELIVERY

1. Generate output following template.md structure
2. Format each model's prompt in code blocks
3. Include metadata and prompt breakdown
4. Write to: `./workspaces/_prompt/prompt-{name}-{date}.md`
5. Verify file write success

**Completion:** Report output path + list of models covered.

> Workspace-independent — no workspace state update required.

**After delivery → control returns to orchestrator.**
