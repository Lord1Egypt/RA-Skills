## Description:

Reviews submitted code snippets and diffs for defects, security concerns, performance, and style, then drafts prioritized feedback, suggested fixes, and a quality score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gechengling](https://clawhub.ai/user/gechengling)

### License/Terms of Use:

MIT-0

## Use Case:

Software developers and reviewers use this skill to examine submitted code snippets or diffs and prepare advisory review comments, security and quality findings, and possible fixes. A human reviewer should verify findings before acting on them; the skill does not execute code, edit repositories, or connect to code hosting platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and reported a possible mismatch involving database queries and user records.

Mitigation: Check that database-query guidance fits the submitted code and independently verify recommendations involving user records.

Risk: Review comments and suggested fixes may not account for call paths, configuration, or deployment details outside the submitted code.

Mitigation: Share only the code needed for review, redact sensitive details, and have a qualified reviewer confirm findings against the wider application before acting.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown review comments with inline code examples and a structured quality score]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory findings and suggested fixes for submitted snippets or diffs; no code execution, repository edits, or external posting.]

## Skill Version(s):

3.0.5 (source: SKILL.md frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
