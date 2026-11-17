## Description:

Locally evaluates password strength by length, character variety, estimated entropy, and common weakness checks, then returns a score and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security educators, and users can use this skill to run a local Chinese-language password strength check before account registration, password hygiene reviews, or customer security guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real passwords supplied as command-line arguments or batch-list entries can be captured in shell history, process listings, terminal output, CI logs, or shared session logs.

Mitigation: Prefer sample passwords for routine checks; avoid sensitive credentials in shared terminals, CI jobs, or logged environments; mask or remove batch output before testing real credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-password-strength)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text or Markdown with local Python CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language guidance; local standard-library Python execution; password values may appear in terminal history, logs, or batch output.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
