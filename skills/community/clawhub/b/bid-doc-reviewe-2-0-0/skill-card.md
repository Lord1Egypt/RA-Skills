## Description:

A China tendering-law document review assistant that checks bid notices, prequalification files, bid documents, invitations, clarifications, evaluation reports, and candidate award notices for compliance risks using referenced tendering knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, tendering, and compliance users use this skill to review China tendering documents, identify procedural and substantive compliance risks, and produce prioritized remediation guidance. It is intended as an AI-assisted review aid and not as a substitute for formal legal advice or the legal responsibilities of tendering parties.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated review reports may be mistaken for formal legal advice or may be applied outside PRC tendering law.

Mitigation: Treat outputs as AI-assisted review only, confirm the matter is within PRC tendering law, and have qualified professionals review conclusions before action.

Risk: The skill requires referenced knowledge bases and may produce incomplete or stale legal conclusions when those sources do not cover the issue or recent rules.

Mitigation: Verify cited sources, check current laws and local rules, and escalate unavailable or time-sensitive legal questions to counsel or the relevant regulator.

Risk: Generated reports include mandatory author and WeChat promotional signature text.

Mitigation: Remove or ignore the promotional signature when it is not appropriate for the deployment or final report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-doc-reviewe-2-0-0)
- [招投标实务与合规 knowledge base](https://ima.qq.com/wiki/?shareId=6bd8e274955cb1493860613dbaed87ceb170158b2ac6ac32bbca7f9a4f534a6a)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown compliance review report with risk tables, legal-source labels, disclaimers, and action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask up to three structured follow-up questions for missing required project information; quick-response mode summarizes high risks first for long or urgent documents.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
