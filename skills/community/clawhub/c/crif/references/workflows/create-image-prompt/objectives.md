# CREATE IMAGE PROMPT

> **CRIF - WORKFLOW OBJECTIVES**
> **NAME:** Create Image Prompt (create-image-prompt)
> **PURPOSE:** Define WHAT this workflow must achieve (mission, objectives, validation, deliverables)

---

## MISSION

Translate user's visual intent into precise, copy-paste ready AI image prompts optimized for specific generation models. Delivers technically accurate prompts with proper composition design, style consistency, and model-specific parameters that produce predictable, high-quality visual outputs. Enables users to generate images matching their creative vision through clear prompts with comprehensive technical guidance and optional variants.

---

## OBJECTIVES

1. **Clarify Visual Intent & Gather Complete Requirements** - Analyze user request, gather all required parameters (subject, style, purpose) and relevant optional parameters through natural dialogue, apply smart defaults where appropriate, and confirm understanding before proceeding

2. **Read & Apply Style Definition** - Read style guidelines from library or extract from user's custom description, internalize style rules covering visual characteristics and composition principles, analyze reference images if provided

3. **Design Visual Composition** - Plan composition layout applying visual principles, determine camera angle and framing, design depth layering, plan negative space if required, establish focal point and visual flow

4. **Construct Layered Prompt Using Image-Prompt-Engineering Guide** - Apply guide methodology to build prompt in layers covering subject, style, composition, lighting, color palette, mood, and technical quality markers

5. **Optimize for Target AI Models** - Apply model-specific guidance to adapt prompt structure and syntax for each target model, generate optimized versions per specified models (or default 4: Universal, ChatGPT, Gemini, Grok)

6. **Generate Prompt Variants (If Requested)** - Create specified number of variations maintaining style consistency while introducing controlled diversity through composition angles, lighting conditions, color palette variations, or mood intensities

7. **Define Technical Parameters & Settings** - Specify aspect ratio, quality settings, style intensity parameters, negative space handling, output resolution recommendations

8. **Format Output as Copy-Paste Ready** - Follow template structure with clear organization, format each model's prompt for direct copy-paste with zero editing required

---

## METHODOLOGY PRINCIPLES

image-prompt-engineering: `./references/guides/image-prompt-engineering.md`

**Autonomous Execution:** Full autonomy on clarification paths, prompt construction strategies, composition designs, and optimization techniques.

**Phased Approach:**
- Phase 1: Understanding & Clarification (gather requirements)
- Phase 2: Style & Composition Planning
- Phase 3: Prompt Construction
- Phase 4: Model Optimization
- Phase 5: Variant Generation (if requested)
- Phase 6: Formatting & Guidance

**Required Parameters:** subject, style, purpose
**Optional Parameters (smart defaults):** target_model, aspect_ratio, camera_angle, framing, negative_space, mood, color_palette, lighting, number_of_variants, additional_details

**Language Requirement:** All image prompts MUST be written in English, regardless of `{language_output}` setting.

---

## VALIDATION CRITERIA

- [ ] **Style & Composition Quality:** Subject clearly described, style consistency maintained, composition well-designed with appropriate focal point
- [ ] **Model Optimization:** Prompts optimized for specified models (or default 4: Universal/ChatGPT/Gemini/Grok), syntax matches model preferences
- [ ] **Copy-Paste Readiness:** Each primary prompt ready for direct use with zero editing, all prompts complete and standalone

---

## DELIVERABLES

- **Primary output:** `{output_path}`
  - Format: `{output_format}`
  - Language: English (required for AI image models)

---

**EXECUTION:** Autonomous phased approach (no shared component - workspace-independent workflow)

---

*Philosophy: Autonomous execution + Image-prompt-engineering guide + Phased approach + Copy-paste ready outputs + Multi-model optimization + Token efficiency*
