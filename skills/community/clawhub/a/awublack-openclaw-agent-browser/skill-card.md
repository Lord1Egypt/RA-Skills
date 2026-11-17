## Description:

Awublack Openclaw Agent Browser lets an OpenClaw assistant call a locally installed agent-browser CLI to fetch a web page and return its title and extracted content as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awublack](https://clawhub.ai/user/awublack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an OpenClaw assistant retrieve web page titles and page content through a local browser CLI for summarization or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes a local browser command and the security evidence calls for argument-safe subprocess execution and URL validation.

Mitigation: Review before use, restrict inputs to trusted URLs, and update the script to validate URLs and pass arguments without shell interpolation.

Risk: The documentation claims fully local processing, while browser access still involves external network requests to the requested sites.

Mitigation: Treat use as network activity and avoid sensitive URLs until external network exposure is documented and reviewed.

Risk: The skill depends on an unpinned global agent-browser installation.

Mitigation: Pin or vendor the browser dependency and verify the package source before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/awublack/skills/awublack-openclaw-agent-browser)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured JSON containing success, url, title, content, and summary fields; content is extracted from Markdown CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a locally installed agent-browser CLI; the browser command is time-limited by the script.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
