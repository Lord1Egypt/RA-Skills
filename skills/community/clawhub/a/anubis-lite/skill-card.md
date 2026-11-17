## Description:

Anubis Lite -- Career Application Engine. Paste a job description and get tailored resume bullet points in seconds. Free tier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career-support agents use this skill to analyze a pasted job description, extract ATS keywords, and draft tailored resume bullets and a positioning statement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install step uses system Python package installation behavior.

Mitigation: Run dependency installation in a virtual environment instead of modifying the system Python environment.

Risk: Pasted job descriptions may be confidential if transcripts or logs are retained or shared.

Mitigation: Avoid pasting confidential postings unless the execution environment and transcript handling are approved for that data.

Risk: The skill output includes a paid upgrade promotion.

Mitigation: Review generated output before sharing and remove promotional text when it is not appropriate for the deployment context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/occupythemilkyway/skills/anubis-lite)
- [ClawHub homepage metadata](https://clawhub.ai/occupythemilkyway/anubis-lite)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks plus generated career-application text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JOB_DESCRIPTION input and produces an ATS keyword report, five tailored resume bullets, and a positioning statement.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
