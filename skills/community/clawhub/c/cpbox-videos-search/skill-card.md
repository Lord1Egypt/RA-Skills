## Description:

Searches for videos and returns title, URL, thumbnail, duration, view count, and creator metadata, with freshness filters, SafeSearch, and pagination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to search video content and retrieve structured video metadata for research, monitoring, curation, and platform-specific discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill routes video-search queries through a paid external service.

Mitigation: Confirm the provider data flow and avoid sensitive search terms unless that external transmission is acceptable.

Risk: Use can trigger automatic paid searches.

Mitigation: Confirm wallet configuration and payment limits before enabling automatic payment flows.

Risk: The skill tells users to run an unpinned payment helper package.

Mitigation: Use a pinned and verified version of the payment helper before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-videos-search)
- [x402 payment setup steps](https://github.com/springmint/cpbox-skills#prerequisites)
- [CPBox API provider](https://www.cpbox.io)
- [CPPay facilitator](https://www.cppay.finance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON video-search response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented service returns structured JSON video results from a paid external API.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
