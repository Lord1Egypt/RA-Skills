## Description:

Checks URL health status, including HTTP response codes, redirects, broken links, and server errors, using the Python standard library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content maintainers, and site operators use this skill to check whether URLs are reachable, inspect HTTP status codes, and identify broken links or server errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make unrestricted outbound URL checks from the agent runtime to any supplied URL.

Mitigation: Use it only in runtimes where outbound egress is acceptable, and avoid localhost, private-network, cloud metadata, credential-bearing, or untrusted redirecting URLs unless egress controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-url-health-checker)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key required.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
