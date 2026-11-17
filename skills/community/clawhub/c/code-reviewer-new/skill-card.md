## Description:

Reviews Python code for quality, style, and common bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dapan0902](https://clawhub.ai/user/dapan0902)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review Python code against a checklist for syntax, error handling, type annotations, PEP 8 style, imports, comments, redundancy, loops, and naming. It returns prioritized findings with severity, rationale, suggested fixes, a score, and top recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger wording may be too broad for non-Python code review requests.

Mitigation: Confirm the requested review target is Python or state when the checklist may not apply.

Risk: The source checklist is Chinese-only, which may reduce review transparency for non-Chinese-speaking users or reviewers.

Mitigation: Have reviewers who do not read Chinese validate the checklist with a trusted translation before relying on it.

## Reference(s):

- [Python code review checklist](artifact/references:review-checklist.md)
- [ClawHub skill page](https://clawhub.ai/dapan0902/skills/code-reviewer-new)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown review with severity-grouped findings, score, recommendations, and corrected code snippets when applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focused on Python code review; parts of the source checklist are Chinese-only.]

## Skill Version(s):

1.0.3 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
