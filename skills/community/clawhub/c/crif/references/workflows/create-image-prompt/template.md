<!--
CREATE IMAGE PROMPT TEMPLATE
INSTRUCTIONS:
- image-prompt-engineering: `./references/guides/image-prompt-engineering.md`
- Validation: See create-image-prompt/objectives.md

LANGUAGE:
- Output: English (required for AI image generation models)

TERMINOLOGY:
- All prompts must be in English for optimal AI model performance
- Technical terms should follow model-specific conventions
-->

# {WORKFLOW_OUTPUT_TITLE}

**Main topic:** {1 sentence describing the research subject/topic}
**AI Model:** {ai-model-name}

═══════════════════════════════════════════════════════════════════

# PRE-DELIVERY VALIDATION CHECKLIST

> **Reference:** See detailed validation checklist in `create-image-prompt/objectives.md` - Section "Pre-delivery validation"

**Validation result:** ☐ Passed / ☐ Failed

**Issues/blockers (if failed):**
- {List any blockers preventing delivery}

**Proceed to content generation:** ☐ Yes / ☐ No

═══════════════════════════════════════════════════════════════════

# WORKFLOW OUTPUT CONTENT

> This section structure is a generic template. Each workflow should customize the specific sections based on its objectives and scope.
>
> **Language Requirement:** All content between `<!-- BEGIN OUTPUT CONTENT -->` and `<!-- END OUTPUT CONTENT -->` markers must be written in **EN - English**.

<!-- BEGIN OUTPUT CONTENT -->

---

## 📋 METADATA

<!-- Display all parameters collected from user during STEP 0 interaction -->
<!-- This provides context for understanding the prompts below -->

**Subject:** {subject}
<!-- Main subject/concept for the image as provided by user -->

**Style:** {style_name}
<!-- Visual style name from styles library (e.g., "voxel-art", "cyberpunk-neon") -->

**Purpose:** {purpose}
<!-- Use case/purpose for the image (e.g., "social media post", "blog header", "logo") -->

**Models:** {target_models}
<!-- List of target models (default: "Universal, ChatGPT Image, Gemini Image, Grok Image") -->

**Parameters:**
- Aspect Ratio: {aspect_ratio}
- Camera Angle: {camera_angle}
- Framing: {framing}
- Negative Space: {negative_space}
- Mood: {mood}
- Color Palette: {color_palette}
- Lighting: {lighting}
- Variants: {number_of_variants}
<!-- Display all optional parameters (use "Default" or "Not specified" if user didn't provide) -->

**Style Reference:** {style_file_path}
<!-- Path to style file used (e.g., "workflows/create-image-prompt/styles/voxel-art.md") or "Custom style" -->

**Reference Images:** {reference_images_provided}
<!-- "User provided [count] reference images" or "No reference images" -->

---

## 🎨 PRIMARY PROMPTS

<!-- CRITICAL: Each model section must be COMPLETE and COPY-PASTE READY -->
<!-- User should be able to copy entire code block and use immediately -->

### Universal Prompt (Midjourney / Stable Diffusion)

<!-- Midjourney/SD format: prompt text + inline parameters -->
<!-- Include --ar (aspect ratio), --q (quality) -->
<!-- Example: "A serene landscape --ar 16:9 --q 2" -->

```
{universal_prompt_text} --ar {aspect_ratio} --q {quality}
```

### ChatGPT Image (DALL·E 3)

<!-- DALL·E 3: Natural language prompt only, NO inline parameters -->
<!-- Settings are separate UI fields - display them clearly -->

```
{chatgpt_prompt_text}

--- Settings ---
Size: {dalle_size}
Quality: {dalle_quality}
Style: {dalle_style}
```

<!--
DALLE SIZE OPTIONS:
- 1024x1024 (square)
- 1792x1024 (landscape)
- 1024x1792 (portrait)

DALLE QUALITY: standard | hd
DALLE STYLE: natural | vivid
-->

### Gemini Image (Imagen 3)

<!-- Imagen 3: Natural language prompt, settings in UI -->
<!-- Safety filter may block some prompts - use BLOCK_ONLY_HIGH -->

```
{gemini_prompt_text}

--- Settings ---
Aspect Ratio: {gemini_aspect_ratio}
Safety Filter: BLOCK_ONLY_HIGH
```

<!--
GEMINI ASPECT RATIO OPTIONS:
- 1:1, 3:4, 4:3, 9:16, 16:9
-->

### Grok Image (Flux)

<!-- Flux: Settings: aspect ratio, guidance scale, steps -->

```
{grok_prompt_text}

--- Settings ---
Aspect Ratio: {flux_aspect_ratio}
Guidance Scale: {flux_guidance}
Steps: {flux_steps}
```

<!--
FLUX PARAMETERS:
- Aspect Ratio: 1:1, 16:9, 9:16, 4:3, 3:4, 21:9
- Guidance Scale: 3.0-15.0 (recommended: 7.5)
- Steps: 20-50 (recommended: 28)
-->

---

## 🎭 VARIANT PROMPTS (if requested)

<!-- CONDITIONAL: Only populate if user requested variants (number_of_variants > 1) -->
<!-- Each variant should maintain style consistency but explore different angles/moods/compositions -->
<!-- Format: Copy structure from PRIMARY PROMPTS above, one variant at a time -->
<!-- If number_of_variants = 1, write: "No variants requested" -->

{variant_prompts_section}

<!--
VARIANT GENERATION GUIDELINES:
- Maintain core subject and style
- Vary: composition, mood, lighting, camera angle, or color emphasis
- Each variant should be equally complete (all 4 models)
- Label clearly: "Variant 1: [brief description]", "Variant 2: [brief description]"

EXAMPLE STRUCTURE:
### Variant 1: [Description]

#### Universal
[prompt with params]

#### ChatGPT
[prompt with settings]

... (repeat for all models)
-->

---

## 🔍 PROMPT BREAKDOWN

<!-- Explain HOW the prompt was constructed - help user understand for manual editing -->
<!-- Keep this section brief and actionable -->

**Core Components:**
{prompt_components_list}
<!-- List main elements in bullet format, e.g.:
- Subject: voxel art landscape
- Environment: floating islands
- Key objects: waterfalls, trees, crystals
-->

**Style Elements:**
{style_elements_applied}
<!-- List style-specific characteristics applied, e.g.:
- Blocky, cubic geometry (voxel style)
- Vibrant color palette
- Isometric perspective
- Smooth gradients on surfaces
-->

**Composition:**
{composition_description}
<!-- Describe visual arrangement decisions, e.g.:
- Camera: Isometric view from 45° angle
- Framing: Wide shot showing full scene
- Negative space: Top 20% reserved for text overlay
- Focal point: Central island with waterfall
- Lighting: Soft ambient with golden hour glow
-->

---

*Generated by CRIF Image Creator Agent*


<!-- END OUTPUT CONTENT -->
