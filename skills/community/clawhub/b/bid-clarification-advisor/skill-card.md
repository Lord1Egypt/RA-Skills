## Description:

Helps Chinese procurement bidders respond to clarification, explanation, or correction requests by checking whether the request is lawful, identifying response boundaries, and drafting compliant response and follow-up materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement and bid teams use this agent when they receive a clarification letter and need structured analysis of the request, safe response wording, records to preserve, and possible challenge or complaint next steps. The skill is tailored to Chinese bidding, government procurement, and state-owned enterprise procurement contexts.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The agent may produce incorrect, incomplete, or outdated procurement-law guidance.

Mitigation: Review outputs against current law, project documents, and qualified professional judgment before acting.

Risk: The workflow depends on configured Chinese procurement knowledge bases and may mark unsupported conclusions as needing source verification.

Mitigation: Confirm cited knowledge-base material and require current project-file or legal authority for any unlawful-request finding.

Risk: Generated responses include a fixed signature disclosed in the security evidence.

Mitigation: Change or override the signature in the host workflow if that attribution is not appropriate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-clarification-advisor)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown report with analysis, response draft, recordkeeping checklist, and follow-up options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include legal-source reminders, a disclaimer, and a fixed signature.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact manifest and SKILL.md report 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
