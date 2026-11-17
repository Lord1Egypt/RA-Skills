## Description:

Audit and fix provenance in knowledge base notes. Ensure every factual claim has an inline citation with date and source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjjhenriksen](https://clawhub.ai/user/jjjhenriksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and knowledge base maintainers use this skill to audit notes for missing or malformed inline citations, broken reference links, and provenance gaps. It drafts grouped fixes and summary reports while requiring approval before applying edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Draft citation fixes or batch edits could change knowledge base notes incorrectly.

Mitigation: Review proposed fixes before applying them and keep batch edits behind explicit user approval.

Risk: Uncited factual claims may lack enough evidence to repair automatically.

Mitigation: Flag missing citations instead of fabricating sources, and require a valid source before completing the fix.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown citation audit report with grouped draft fixes and counts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; proposed batch edits require user approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
