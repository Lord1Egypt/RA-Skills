## Description:

This skill helps agents perform privacy-focused DDGS metasearch across webpages, news, images, videos, and books without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idkwhodatis](https://clawhub.ai/user/idkwhodatis)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add real-time web, news, image, video, and book search to agents through DDGS, with configurable region, safesearch, time limit, result count, backend, and proxy settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms may be sent to external search services and could expose secrets, private identifiers, or internal-only information.

Mitigation: Avoid using sensitive queries and deploy the skill only where external search traffic is acceptable.

Risk: The installation guidance uses an unpinned ddgs package, which can change behavior across releases.

Mitigation: Install in an isolated virtual environment and use a reviewed pinned package version for governed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/idkwhodatis/skills/ddgs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search behavior can be configured by query type, region, safesearch level, time limit, result count, backend, and proxy settings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
