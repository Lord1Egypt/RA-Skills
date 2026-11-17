## Description:

Generate high-quality anime style illustrations. Use when the user asks for anime, light novel covers, or japanese animation style art.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate anime-style illustrations, light novel covers, and Japanese animation style art through a WeryAI-backed image generation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-handling risk from providing this skill a WeryAI API key.

Mitigation: Provide the key through a protected environment or secret store, avoid command-line API key arguments, and persist it only when explicitly needed.

Risk: Runtime-execution risk from running a Bun-based CLI.

Mitigation: Review or pin the runtime before using the generate script, and install the skill only when this execution model is acceptable.

Risk: Optional webhook URLs and local image-skill config can expand data exposure or local write behavior.

Mitigation: Avoid webhook URLs unless required, review the destination before use, and keep project or home configuration scoped to this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/632657122/skills/anime-image-generator)
- [Gateway Alignment Notes](references/weryai-platform.md)
- [Style Presets](references/style-presets.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Model Registry Schema](references/config/model-registry-schema.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [WeryAI API introduction](https://docs.weryai.com/en)
- [WeryAI text-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-text-to-image-task)
- [WeryAI image-to-image API](https://docs.weryai.com/api-reference/image-generation/submit-image-to-image-task)
- [WeryAI task status API](https://docs.weryai.com/api-reference/tasks/query-task-details)
- [WeryAI API keys](https://weryai.com/api/keys)
- [WeryAI call history](https://weryai.com/api/history)

## Skill Output:

**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Downloaded image files with optional JSON summaries and Markdown-facing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IMAGE_GEN_API_KEY and may write local image-skill configuration.]

## Skill Version(s):

2026.3.23 (source: server release metadata; SKILL.md frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
