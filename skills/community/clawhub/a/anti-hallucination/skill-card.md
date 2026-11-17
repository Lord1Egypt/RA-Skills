## Description:

Prevents AI from fabricating facts by requiring source-based responses: if a claim is not supported by records, the agent should say it is not sure instead of inventing details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiping3](https://clawhub.ai/user/yiping3)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to make an AI assistant check available records before making factual claims, cite sources when support exists, and decline or ask for clarification when support is missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local-record checks could expose private memory, documents, or knowledge-base content.

Mitigation: Configure an explicit source allowlist and confirm requester authorization before the agent inspects or cites local records.

Risk: Source citations may reveal sensitive filesystem paths or internal document locations.

Mitigation: Use approved citation formats and avoid exposing sensitive paths unless the environment and audience permit it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiping3/skills/anti-hallucination)
- [Publisher profile](https://clawhub.ai/user/yiping3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Plain text or Markdown with source citations, uncertainty statements, and optional JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed to make the agent cite approved records for supported claims and withhold unsupported factual assertions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
