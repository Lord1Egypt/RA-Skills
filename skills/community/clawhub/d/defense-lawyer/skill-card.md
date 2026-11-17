## Description:

AI-powered criminal defense assistant for the Chinese legal system that supports case analysis, defense strategy formulation, evidence assessment, legal research, sentencing analysis, and legal document drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

External legal professionals and developers use this skill to structure criminal-defense analysis for Chinese-law matters, including evidence review, strategy options, sentencing considerations, and draft defense documents. Outputs are legal-assistance drafts and require licensed attorney review before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process highly sensitive criminal-defense facts, client identities, privileged information, evidence details, detention status, or confession information.

Mitigation: Use only in an approved secure environment, avoid entering real client-identifying or privileged facts unless authorized, and follow internal legal data-handling controls.

Risk: Installation relies on an unpinned external Python package.

Mitigation: Install in a virtual environment or sandbox, verify the package source and version before use, and review package contents before deployment.

Risk: Generated legal analysis, citations, strategy recommendations, and filings may be incomplete, inaccurate, or unsuitable for a specific case.

Mitigation: Treat outputs as drafts and require review by a licensed attorney before relying on them or filing any document.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhenstaff/skills/defense-lawyer)
- [Publisher profile](https://clawhub.ai/user/zhenstaff)
- [Project homepage](https://github.com/ZhenRobotics/openclaw-defense-lawyer)
- [Project issues](https://github.com/ZhenRobotics/openclaw-defense-lawyer/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce legal analysis, strategy recommendations, evidence assessments, sentencing considerations, and draft legal documents.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and README state 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
