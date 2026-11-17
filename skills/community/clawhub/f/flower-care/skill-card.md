## Description:

Identifies flowers or plants from an uploaded image, provides care guidance across watering, light, temperature, soil, fertilizing, and pest control, and can generate an interactive HTML care report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and gardening assistants use this skill to identify plants from photos, review plant health, and receive practical care guidance. It can also answer common plant-care questions from its bundled reference database without an image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant images are sent to DashScope during image-based identification.

Mitigation: Use only trusted, non-sensitive plant images and disclose the external processing path to users before submitting images.

Risk: Credential handling can draw from environment variables or local configuration, and the security evidence advises avoiding environments where OPENAI_API_KEY is present.

Mitigation: Use a dedicated DashScope API key with limited scope, keep it out of shared shells, and avoid running the skill in environments containing unrelated API keys.

Risk: Generated HTML reports persist the uploaded image and may be unsafe to open from untrusted inputs until the HTML escaping issue is fixed.

Mitigation: Open reports only for trusted inputs, store reports in controlled locations, and review or sanitize report HTML before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/flower-care)
- [Project homepage from release metadata](https://github.com/bettermen/flower-care)
- [Plant care database](references/plant_care_db.md)
- [DashScope API key console](https://dashscope.console.aliyun.com/apiKey)
- [DashScope compatible-mode chat completions endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown summary, shell commands, configuration guidance, JSON-derived plant analysis, and an HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DashScope API key for image-based identification; text-only plant-care queries can use the bundled reference database.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
