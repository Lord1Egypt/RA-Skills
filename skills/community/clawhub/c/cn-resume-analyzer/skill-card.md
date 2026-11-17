## Description:

Analyzes Chinese resume content and returns structured scoring, keyword coverage, format checks, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to review Chinese resumes for completeness, keyword coverage, formatting, and actionable improvements before job applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume text can contain personal data, and the skill workflow may accept pasted text, file paths, or URLs.

Mitigation: Prefer pasted resume text and only provide file paths or URLs when you intentionally want the agent to read or fetch that document.

Risk: Optional remote resume retrieval may require installing an unpinned dependency.

Mitigation: Avoid optional dependencies unless remote retrieval is required, and review the dependency before installing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-resume-analyzer)
- [AISoBrand](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown text with structured resume score, matched sections, summary, and improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese-language scoring labels and resume improvement recommendations.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
