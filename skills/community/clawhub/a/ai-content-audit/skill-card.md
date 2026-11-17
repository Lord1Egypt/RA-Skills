## Description:

Audits a content library, docs site, or blog for low-quality AI-generated filler that may erode trust and search performance, then triages what to keep, enrich, rewrite, or delete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Content, SEO, documentation, and publishing teams use this skill to audit scaled content libraries for low-quality filler, evidence gaps, and repeated structures. It produces checkable verdicts and an editorial triage plan for remediation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may analyze internal content and performance data.

Mitigation: Provide only the corpus and metrics needed for the audit.

Risk: Delete-and-redirect recommendations could remove useful content if applied automatically.

Mitigation: Treat deletion and redirect recommendations as human-reviewed editorial guidance before implementation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/ai-content-audit)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/ai-content-audit.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with an audited inventory table, triage plan, and publishing quality gate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses provided corpus, optional performance data, publishing context, and content purpose to produce human-reviewed editorial recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
