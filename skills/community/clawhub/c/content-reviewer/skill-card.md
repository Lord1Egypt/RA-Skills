## Description:

Reviews influencer content submissions against campaign briefs, approved claims, disclosure obligations, platform requirements, and C3 ART criteria, then returns an evidence-linked gate decision and creator-ready revision feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, compliance, and creator-operations teams use this skill to review a frozen influencer deliverable before publication, amplification, or payment milestones. It checks brand fit, message accuracy, disclosure adequacy, claim integrity, platform requirements, and maps revision requests to evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can influence approval, revision, publication, payment, or compliance decisions for influencer content.

Mitigation: Review the audit output before acting on business decisions, and require locked asset, brief, claim, disclosure, platform, and market evidence for scored conclusions.

Risk: In a full repository or plugin setup, the skill may run local scoring or validation scripts.

Mitigation: Inspect the skill and scripts before deployment, run them in a controlled workspace, and avoid scoring or persistence when required runtime assets are unavailable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/content-reviewer)
- [Publisher Profile](https://clawhub.ai/user/aaron-he-zhu)
- [Project Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Standalone Auditor Runtime](artifact/references/auditor-runtime.md)
- [Quality Review Aids](artifact/references/quality-review-aids.md)
- [Review Templates](artifact/references/review-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with structured score states, gate verdicts, and creator revision notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally write a validated v3 audit artifact after user permission; standalone installs fail closed when required scoring assets are unavailable.]

## Skill Version(s):

17.0.0 (source: artifact/SKILL.md frontmatter and evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
