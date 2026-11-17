## Description:

Coordinates a three-agent workflow that analyzes Chinese e-commerce image requests, creates a creative brief, generates AI image drafts, and reviews quality for delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duzhihai123](https://clawhub.ai/user/duzhihai123)

### License/Terms of Use:

MIT-0

## Use Case:

External users, merchants, designers, and agent operators use this skill to turn Chinese e-commerce image requirements into creative briefs, generated image options, quality reviews, and iteration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically run local Jimeng or Liblib automation scripts.

Mitigation: Install and run it only in a contained workspace after confirming the automation scripts are trusted and not writable by other users.

Risk: Prompts and project history may retain confidential product plans or personal data.

Mitigation: Avoid entering confidential, personal, or unreleased business information unless the workspace retention policy is acceptable.

Risk: The built-in quality review should not be treated as a substitute for real image inspection.

Mitigation: Have a human review generated images before publication, especially for brand, legal, marketplace, or safety-sensitive requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duzhihai123/skills/ai-image-team)
- [Jimeng image tool](https://jimeng.jianying.com/)
- [LiblibAI image tool](https://www.liblib.art/)

## Skill Output:

**Output Type(s):** [text, json, image files, guidance]

**Output Format:** [JSON delivery result with image entries, a creative brief, and a quality review.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return clarification questions, iteration guidance, or an error status when requirements are incomplete or generation fails.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
