## Description:

This skill helps users review PRC bidding and tendering documents for compliance risks, conflicts, exclusionary brand or technical requirements, procedural timing issues, and actionable revision guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External users and compliance reviewers use this skill to examine bidding announcements, prequalification files, tender documents, bid invitations, clarification or amendment letters, evaluation reports, and winning-candidate announcements under the PRC bidding-law framework. It produces risk lists, compliance grades, and prioritized modification suggestions, while reminding users to confirm current law and project-specific jurisdiction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated compliance reports could be mistaken for formal legal advice or current jurisdiction-specific regulatory guidance.

Mitigation: Treat outputs as review assistance, confirm project jurisdiction and current rules, and obtain qualified legal or regulatory review before relying on conclusions.

Risk: The skill requires reports to include a third-party signature and WeChat feedback contact that may be unrelated to the user's review task.

Mitigation: Review generated reports before sharing and remove or adapt promotional signature and feedback contact content according to deployment policy.

Risk: Knowledge-base gaps or outdated law could lead to incomplete citations or stale compliance conclusions.

Mitigation: Require conclusions to be anchored to retrieved knowledge-base sources or clearly marked built-in baselines, and verify newer rules when coverage is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-doc-reviewe)
- [招投标实务与合规 knowledge base](https://ima.qq.com/wiki/?shareId=6bd8e274955cb1493860613dbaed87ceb170158b2ac6ac32bbca7f9a4f534a6a)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with tables, risk levels, compliance grading, prioritized recommendations, and disclaimers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask up to three structured clarification questions when required project facts are missing; may summarize high-risk items first for urgent or long-document reviews.]

## Skill Version(s):

1.0.0 (source: server release evidence; artifact manifest and README describe skill implementation version 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
