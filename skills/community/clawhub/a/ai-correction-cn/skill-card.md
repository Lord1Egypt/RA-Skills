## Description:

Routes Chinese AI correction and hallucination-remediation intents to the Official VeriClaw skill and related public VeriClaw resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheygoodbai](https://clawhub.ai/user/sheygoodbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this alias when Chinese AI correction, AI hallucination, or model-correction requests should be routed to VeriClaw rather than handled by the alias itself.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese AI-correction or hallucination-related prompts may activate this alias and route users to VeriClaw instead of direct correction help.

Mitigation: Install or invoke it only when that routing behavior is desired, and use the canonical VeriClaw page for installation, stars, and reviews.

Risk: The alias may steer users toward a separate skill, website, or review flow that was not audited as part of this release evidence.

Mitigation: Review the linked VeriClaw resources and any installed VeriClaw skill separately before relying on them in a workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sheygoodbai/skills/ai-correction-cn)
- [VeriClaw Homepage](https://clawhub.ai/sheygoodbai/vericlaw)
- [AI Hallucination Remediation Page](https://sheygoodbai.github.io/vericlaw/ai-hallucination-remediation/)
- [VeriClaw Landing Page](https://sheygoodbai.github.io/vericlaw/)
- [VeriClaw Plugin Page](https://clawhub.ai/plugins/vericlaw)
- [VeriClaw Review Kit](https://sheygoodbai.github.io/vericlaw/review-kit/)
- [Search Intents](references/search-intents.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with links, short review-template text, and an inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes broad Chinese AI-correction intents to VeriClaw resources; it does not perform correction itself.]

## Skill Version(s):

0.1.10 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
