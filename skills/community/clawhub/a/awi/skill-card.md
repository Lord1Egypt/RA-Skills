## Description:

AWI provides zero-config web page reading and DuckDuckGo search through a single binary, with fallback from direct requests to adapted fetching and browser rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzocb](https://clawhub.ai/user/jzocb)

### License/Terms of Use:


## Use Case:

Developers and agent users can use AWI to fetch web page content, run DuckDuckGo searches, and batch-read URL lists from an agent workflow without API keys or Docker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and immediately runs an unverified external binary from the upstream GitHub release for the user's platform.

Mitigation: Review the upstream repository and release process before installing, and avoid using the tool with private URLs or sensitive search terms unless external requests and browser rendering are acceptable.

## Reference(s):

- [AWI ClawHub skill page](https://clawhub.ai/jzocb/skills/awi)
- [AWI upstream homepage](https://github.com/jzOcb/awi)
- [AWI v0.1.0 Linux AMD64 release binary](https://github.com/jzOcb/awi/releases/download/v0.1.0/awi-linux-amd64)
- [AWI v0.1.0 macOS ARM64 release binary](https://github.com/jzOcb/awi/releases/download/v0.1.0/awi-darwin-arm64)
- [AWI v0.1.0 macOS AMD64 release binary](https://github.com/jzOcb/awi/releases/download/v0.1.0/awi-darwin-amd64)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return web content in JSON, Markdown, or plain text through the installed awi binary.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
