## Description:

Scans websites and files for broken links with HTTP status details for audits, broken URL discovery, and reference validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site maintainers, and documentation authors use Deadlink to audit URLs in pages and files, identify broken links, inspect redirect behavior, and generate plain-text reports with HTTP status details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound web requests to user-provided URLs and URLs discovered during scans.

Mitigation: Run it only where those requests are acceptable, and avoid untrusted inputs that could trigger requests to localhost, private networks, or cloud metadata services.

Risk: Generated reports are saved as plain text in the current directory.

Mitigation: Run the skill from an appropriate working directory and review generated reports before sharing or retaining them.

## Reference(s):

- [Deadlink ClawHub page](https://clawhub.ai/bytesagain3/skills/deadlink)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files]

**Output Format:** [Markdown guidance with shell command examples and plain-text link check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and network access; reports are saved as timestamped plain-text files in the current directory.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
