## Description:

Query browser compatibility for CSS/JS features using caniuse-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouqicf](https://clawhub.ai/user/zhouqicf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query browser support for CSS, JavaScript, and web platform features, then summarize compatibility status, partial support notes, and practical fallback advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided feature names could be unsafe if interpolated into a shell command.

Mitigation: Run caniuse with literal arguments or known feature identifiers, and avoid shell-string interpolation.

Risk: A global npm installation can alter the developer or agent runtime environment.

Mitigation: Prefer a pinned, project-local installation of caniuse-cli when possible.

## Reference(s):

- [Can I Use](https://caniuse.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with CLI command examples, compatibility summaries, and practical advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include caniuse-cli compatibility tables and notes from the queried feature.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
