## Description:

Fetches financing event lists from the iYiou skill API, deduplicates records, and generates daily or recent 2-7 day Chinese investment reports in Markdown to stdout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-byte](https://clawhub.ai/user/ai-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to fetch public financing-event data, clean and deduplicate records, and produce Chinese daily or recent-window investment reports. The agent may append a final investment-event summary after the script-generated event list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts api.iyiou.com and report content depends on third-party financing-event data.

Mitigation: Use the skill only when that outbound API access is acceptable, and treat generated event text and source links as untrusted third-party content.

Risk: Markdown output includes event text and source links from upstream data.

Mitigation: Review reports before sensitive use, and add Markdown escaping plus HTTPS URL validation before embedding the output in higher-trust workflows.

## Reference(s):

- [Field Mapping](references/field_mapping.md)
- [iYiou skill API endpoint](https://api.iyiou.com/skill/info)
- [ClawHub skill page](https://clawhub.ai/ai-byte/skills/daily-investment-digest)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration]

**Output Format:** [Markdown report text printed to stdout, with optional JSON passed between fetch and render scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scripts do not write report artifacts to disk; final responses should keep event entries first and append exactly one 投资事件总结 section at the end.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
