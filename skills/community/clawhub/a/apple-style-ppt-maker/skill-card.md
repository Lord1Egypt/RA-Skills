## Description: <br>
Create Apple-style minimalist presentation slides through a strict JSON-first workflow that clarifies requirements, locks topic, content, and structure, produces per-slide text and visual specifications, generates 2K WebP images, supports page-level regeneration, and exports the final deck to PPTX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[herve-clawd](https://clawhub.ai/user/herve-clawd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers can use this skill to turn presentation requirements into a reviewed slide plan, generate consistent Apple-style slide images, selectively regenerate individual pages, and export a finished PowerPoint deck. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved deck content is sent to Gemini for image generation. <br>
Mitigation: Review the complete slides_plan.json before rendering and avoid regulated, secret, or otherwise sensitive content unless the deployment context permits that external processing. <br>
Risk: Prompts, slide metadata, generated images, and manifests are saved in the output directory. <br>
Mitigation: Treat the output directory as project data, keep secrets out of deck content, and avoid sharing outputs that contain confidential prompts or metadata. <br>
Risk: API credentials may be loaded from APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY, GEMINI_API_KEY, or a local .env file. <br>
Mitigation: Use a dedicated API key and keep any .env file out of shared folders and version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/herve-clawd/apple-style-ppt-maker) <br>
- [Publisher profile](https://clawhub.ai/user/herve-clawd) <br>
- [Apple Minimal Presentation Spec](references/apple-style-spec.md) <br>
- [Slides schema](references/slides-schema.json) <br>
- [Slides plan template](references/slides-plan-template.json) <br>
- [AI product strategy showcase plan](references/ai-product-strategy-showcase-plan.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON slide plans, shell commands, generated WebP slide images, metadata files, prompts, manifests, and PPTX exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and either APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY or GEMINI_API_KEY; default slide image output is 2K WebP at 16:9.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
