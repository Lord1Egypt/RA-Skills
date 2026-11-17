## Description:

Create Apple-style minimalist presentation slides through a strict JSON-first workflow. Use when an agent must clarify user requirements, lock topic/content/structure, produce per-slide text plus visual specifications, generate 2K WebP images (Nano Banana Pro), support page-level redesign/regeneration, and export the final deck to PPTX.

This skill is ready for commercial/non-commercial use.

## Publisher:

[herve-clawd](https://clawhub.ai/user/herve-clawd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and presentation authors use this skill to gather deck requirements, build a validated slide plan, generate Apple-style slide images, regenerate selected pages, and export a PPTX deck.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential scope: security evidence notes that the skill may search more broadly than documented for local .env files before sending slide prompts to Google's image API.

Mitigation: Set APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY directly in the environment and run from a clean working directory without unrelated parent .env files.

Risk: External API exposure: slide text and visual prompts are sent to Google GenAI for image generation.

Mitigation: Review and sanitize the slide plan before rendering, and avoid sensitive content unless use with Google GenAI is approved for the project.

Risk: Generated slides may contain inaccurate, misleading, or off-brand text or imagery.

Mitigation: Review the full JSON plan before generation and inspect generated images before sharing; regenerate specific slides when corrections are needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/herve-clawd/skills/apple-style-ppt-maker)
- [Apple Minimal Presentation Spec](references/apple-style-spec.md)
- [Slides schema](references/slides-schema.json)
- [Slides plan template](references/slides-plan-template.json)
- [AI product strategy showcase plan](references/ai-product-strategy-showcase-plan.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Conversational guidance, JSON slide plans, Markdown prompts, generated slide image files, metadata JSON, and PPTX exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and a Gemini API key; defaults to 16:9, 2K, WebP slide images before PPTX export.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
