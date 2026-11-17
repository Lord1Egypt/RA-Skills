## Description:

Transforms job description manuals into structured Markdown system prompts for digital employee AI agents using Chudaxia's seven-layer template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charleschor](https://clawhub.ai/user/charleschor)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and AI-agent builders use this skill to convert role or job description manuals from a selected knowledge base into deployable AI-agent system prompts. It supports single-role and batch prompt generation with a required Markdown quality self-check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts may expose sensitive or overly specific internal role information from the selected knowledge base.

Mitigation: Review generated Markdown before sharing or deploying it, and remove company names, people, internal systems, and other sensitive role details.

Risk: Generated prompts may include fixed Chudaxia template attribution or branding.

Mitigation: Confirm that template attribution is acceptable for the intended deployment before publishing or distributing generated prompts.

Risk: Incomplete or ambiguous job descriptions can lead to generic or unsupported role assumptions in the generated prompt.

Mitigation: Check the generated seven-layer prompt against the source job description and require corrections when duties, permissions, KPIs, or boundaries are missing.

## Reference(s):

- [Seven-layer prompt template](references/seven-layer-template.md)
- [Quality checklist](references/quality-checklist.md)
- [ClawHub skill page](https://clawhub.ai/charleschor/skills/chudaxia-ai-coach-position-prompts-generator)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a seven-layer prompt structure and may include a Markdown self-check section or batch summary table.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
