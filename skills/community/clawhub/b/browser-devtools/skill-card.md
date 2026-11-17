## Description:

Browser Devtools is presented as a Chrome Dev Editor-style command-line skill for Chrome Apps and web app development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill to run simple browser-devtools command-line actions such as help, status, configuration, list, add, search, export, and version checks. Evidence flags that the packaged behavior is mostly stubbed or generic, so users should validate it before relying on it for Chrome Dev Editor work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because the bundled scripts appear to be stubs or a generic local logging utility rather than full Chrome Dev Editor functionality.

Mitigation: Review the artifact behavior before installation and confirm the publisher's documented functionality matches the scripts before relying on it.

Risk: Command arguments or added text can be stored under a local browser-devtools data directory.

Mitigation: Avoid passing secrets, tokens, private paths, or sensitive project data, and clear or relocate the data directory when needed.

## Reference(s):

- [Browser Devtools on ClawHub](https://clawhub.ai/xueyetianya/skills/browser-devtools)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text command output with local data and history files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write data.log and history.log under the configured browser-devtools data directory.]

## Skill Version(s):

2.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
