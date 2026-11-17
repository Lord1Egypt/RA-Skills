## Description:

Guides agents in generating customized clothing design drafts from text, reference images, and structured parameters for print-on-demand and manufacturing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, developers, and businesses use this skill to request personalized clothing concepts, print designs, and multi-view previews through the Craftsman clothing design service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Design prompts, reference image URLs, and related metadata are sent to an external design service.

Mitigation: Do not submit secrets or confidential designs; share only material suitable for external processing.

Risk: Generated workspace links may expose design results to anyone with access to the link.

Mitigation: Protect returned share links and distribute them only to intended recipients.

Risk: The optional OneKey CLI is installed from an external package source.

Mitigation: Prefer a pinned version or trusted installation path before using the optional CLI.

## Reference(s):

- [ClawHub dress-designer release](https://clawhub.ai/ai-hub-admin/skills/dress-designer)
- [Craftsman Clothing Designer](https://craftsman-agent.aiagenta2z.com/app/clothing-designer/dress)
- [DeepNLP OneKey access keys](https://www.deepnlp.org/workspace/keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with API request examples and design workspace links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated drafts may include share links, image URLs, design blueprints, and interactive 3D previews when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
