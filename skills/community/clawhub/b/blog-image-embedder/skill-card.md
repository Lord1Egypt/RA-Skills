## Description: <br>
Analyze polished zh-CN blog markdown, generate hero + per-section image prompts, embed image placeholders into the markdown, and save updated version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and blog authors use this skill after polishing zh-CN markdown to add image prompts and image placeholders for a hero image and section images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The input markdown may contain confidential draft content that is processed by LLM or image services. <br>
Mitigation: Confirm the exact markdown file before running and avoid confidential drafts unless that processing is approved. <br>
Risk: Generated prompts or inserted image placeholders may not match the author's intended section structure. <br>
Mitigation: Review the illustrated markdown and generated prompt list before publishing. <br>
Risk: The workflow writes an illustrated markdown file to the configured output directory. <br>
Mitigation: Confirm the output directory before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/blog-image-embedder) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Guidance] <br>
**Output Format:** [JSON object with an illustrated markdown path, generated image prompts, and image paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an illustrated markdown file path, prompt list, and image path list for downstream blog publishing workflows.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
