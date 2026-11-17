## Description:

Provides Tongcheng Chengxin travel search for flights, trains, hotels, buses, attractions, vacation products, itinerary planning, traffic options, and booking links using Tongcheng data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tongcheng-ai](https://clawhub.ai/user/tongcheng-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External-facing travel agents and developers use this skill to answer travel-search requests, compare transportation and lodging options, surface attractions or vacation products, and return booking-oriented results from Tongcheng Chengxin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Returned travel content and booking links may be unsafe or misleading because remote links are not safely validated.

Mitigation: Treat returned UGC, provider text, and links as untrusted, and verify destination domains before clicking.

Risk: Travel queries and optional trip details are sent to Tongcheng's API.

Mitigation: Avoid entering sensitive personal details in free-text travel queries unless this data sharing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tongcheng-ai/skills/chengxin)
- [Tongcheng homepage](https://www.ly.com)
- [API examples](references/api-examples.md)
- [Configuration](references/config.md)
- [Error handling](references/error-handling.md)
- [Output format](references/output-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel-search results with command guidance and booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include remote travel content, UGC, promotional guidance, and provider booking links.]

## Skill Version(s):

0.9.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
