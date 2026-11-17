## Description:

ABTI analyzes how a user talks to AI, assigns one of 28 personality types, and produces a roast-style personality result and shareable card.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindy-youmind](https://clawhub.ai/user/mindy-youmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users run this entertainment-oriented agent skill to analyze available AI chat history and receive an ABTI personality type, roast text, and optional shareable card. Agents can either return a local markdown result or submit derived card data to the ABTI web service when the user explicitly chooses sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an assistant to inspect available chat history, which can include sensitive personal context.

Mitigation: Use only when the user is comfortable with local chat-history analysis, and do not include raw chat excerpts in the result.

Risk: The reviewed artifact refers to additional core instructions that were not present in the artifact.

Mitigation: Review the complete installed skill contents before deployment and prefer local markdown output when the referenced instructions cannot be verified.

Risk: The skill may submit derived result data to an external ABTI endpoint to create a shareable card.

Mitigation: Use external card creation only after explicit user choice; otherwise return the non-HTTP markdown card path.

Risk: Install instructions include unpinned npx commands.

Mitigation: Avoid running unpinned installer commands in high-trust environments without first checking the source and version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mindy-youmind/skills/abti)
- [Publisher profile](https://clawhub.ai/user/mindy-youmind)
- [ABTI website](https://youmind.com/abti)
- [YouMind](https://youmind.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown personality result with optional shareable URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce derived personality type and roast text; source chat content should not be exposed.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
