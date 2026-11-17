## Description:

Design Analysis scans local design image folders and generates structured, interactive HTML presentation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeasonxiang](https://clawhub.ai/user/jeasonxiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and design reviewers use this skill to turn local screenshots or design drafts into a paginated HTML presentation for design review, stakeholder sharing, or archival.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can run active JavaScript when opened.

Mitigation: Create and open reports only from trusted design folders, filenames, and custom section content; do not open or host reports from untrusted inputs on an authenticated or shared origin.

Risk: Invocation parameters may be logged during execution.

Mitigation: Avoid passing secrets or sensitive project details in skill parameters, and review execution logs before sharing them.

Risk: The configured output file can overwrite an existing report.

Mitigation: Choose a new output filename or back up existing reports before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeasonxiang/skills/design-analysis)
- [MDN HTML5 Guide](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Using_HTML5)
- [MDN CSS Flexbox Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout)

## Skill Output:

**Output Type(s):** [code, text, guidance]

**Output Format:** [Standalone HTML document plus JSON-like status summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the report to the requested output path and references local image files by relative path.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
