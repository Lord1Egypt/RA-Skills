## Description:

Deep Reader analyzes books, long documents, and web articles with a layered reading methodology, producing structured interpretation of core ideas, arguments, evidence, and cross-text themes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltryee](https://clawhub.ai/user/ltryee)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Deep Reader to analyze books, long documents, or web articles. The skill supports quick structural scans, detailed argument analysis, and cross-book thematic comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes user-provided books, documents, and URLs, which may contain sensitive or private content.

Mitigation: Provide only files and URLs that are appropriate for the agent to process in the configured environment.

Risk: Broad trigger examples may cause the skill to activate for generic summary, comparison, or article-analysis requests.

Mitigation: Require explicit skill invocation or review activation behavior before deployment in shared agent environments.

## Reference(s):

- [Reading Methodology Reference](artifact/references/reading-methodology.md)
- [ClawHub Skill Page](https://clawhub.ai/ltryee/skills/deep-reader)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reading reports with structured sections, quotations, critique, and optional source links for web articles]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structural notes, conceptual notes, dialectical notes, or web article analysis reports.]

## Skill Version(s):

1.1.0 (source: server release metadata and supplied target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
