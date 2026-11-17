## Description:

Autonomous research assistant for deep research, cross-validation, and cited report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bandwe](https://clawhub.ai/user/bandwe)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to structure multi-source research, evaluate source credibility, synthesize conflicting findings, and produce cited research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may search the web, store research data, create recurring monitoring jobs, or invoke shell-style execution without enough user controls or scope limits.

Mitigation: Set explicit limits for research scope, source count, monitoring duration, storage location, and deletion; require confirmation before any exec command or scheduled task is used.

Risk: Research outputs may include outdated, low-quality, or conflicting source claims.

Mitigation: Use the documented CRAAP scoring, cross-check important claims across sources, label confidence and uncertainty, and include citations with the final report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bandwe/skills/auto-researcher)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Markdown research reports, JSON knowledge graph records, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include source lists, CRAAP credibility scores, confidence labels, contradictory findings, knowledge gaps, and APA or MLA citations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
