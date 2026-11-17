## Description:

A hotel aggregation skeleton that defines multi-platform hotel search, result aggregation, price comparison, and booking workflow interfaces for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-zry](https://clawhub.ai/user/ryan-zry)

### License/Terms of Use:

MIT-0

## Use Case:

Travel assistants and booking agents use this skill to collect a user's city, dates, keywords, and preferred hotel sources, call hotel aggregation functions, and present source-labeled hotel options in Markdown-style tables. Review before real booking use because the security evidence reports unimplemented provider integrations and missing consent/privacy limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate live hotel search, pricing, room detail, and booking capabilities while provider integrations remain incomplete.

Mitigation: Review and implement provider integrations before relying on real availability or pricing, and only present source-provided data with source status clearly identified.

Risk: Travel searches can expose user itinerary details to third-party hotel platforms.

Mitigation: Require explicit user approval before sending city, dates, keywords, preferences, or other travel details to external providers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryan-zry/skills/easy-travel-booking)
- [Publisher profile](https://clawhub.ai/user/ryan-zry)
- [Fenbeitong Open API endpoint](https://openapiv2.fenbeitong.com)
- [Ctrip API endpoint](https://api.ctrip.com)
- [Meituan API endpoint](https://api.meituan.com)
- [Tongcheng API endpoint](https://api.tongcheng.com)
- [Huazhu API endpoint](https://api.huazhu.com)
- [Jinjiang API endpoint](https://api.jinjiang.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Markdown, Guidance]

**Output Format:** [JSON responses and Markdown-style hotel result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; provider calls must be implemented and reviewed before real availability, pricing, room detail, or booking use.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
