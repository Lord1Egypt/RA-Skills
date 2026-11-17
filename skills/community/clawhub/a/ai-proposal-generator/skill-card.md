## Description:

AI Proposal Generator helps agents create professional HTML proposals from meeting notes using built-in proposal styles, color themes, and pricing context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffjhunter](https://clawhub.ai/user/jeffjhunter)

### License/Terms of Use:


## Use Case:

External consultants, agencies, freelancers, and business teams use this skill to turn meeting notes and service or pricing details into client-ready proposal drafts and HTML deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read client meeting notes, proposal pricing files, and global memory while composing proposals.

Mitigation: Ask the agent to show the exact source files it will use and remove unnecessary sensitive inputs before generation.

Risk: Generated HTML can carry unsanitized content derived from meeting notes or untrusted links.

Mitigation: Review and sanitize the generated HTML before sending it to clients or exporting it to PDF.

Risk: Proposal language, scope, pricing, or client commitments may be inaccurate or misleading.

Mitigation: Have a qualified human review the proposal for factual accuracy, business terms, and client suitability before delivery.

## Reference(s):

- [AI Proposal Generator ClawHub page](https://clawhub.ai/jeffjhunter/skills/ai-proposal-generator)
- [Skill instructions](artifact/SKILL.md)
- [Proposal HTML template](artifact/assets/proposal-template.html)
- [Services and pricing template](artifact/assets/SERVICES-template.md)
- [Proposal style templates](artifact/templates/)
- [Proposal color themes](artifact/themes/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown proposal drafts and responsive HTML files with CSS themes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses meeting notes, service/pricing details, selected proposal style, and selected color theme as inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
