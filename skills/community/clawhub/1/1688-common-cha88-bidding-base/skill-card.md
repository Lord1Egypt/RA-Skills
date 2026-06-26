## Description: <br>
Searches 88cha bidding and tender notices by keyword with optional region, date, pagination, and access-key configuration support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search 88cha bidding and tender announcements, format returned results as markdown, and configure the access key required for authenticated searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive access key and may store it through OpenClaw configuration or a local config-file fallback. <br>
Mitigation: Prefer the managed OpenClaw/Gateway secret path, avoid placing AK values in chat or shell history, restrict config-file permissions, and rotate exposed keys. <br>
Risk: Successful CLI runs can send limited usage telemetry to the 1688 gateway. <br>
Mitigation: Review telemetry expectations before deployment in managed or shared environments, especially where usage metadata is sensitive. <br>


## Reference(s): <br>
- [Bidding Search Guide](references/capabilities/bidding_search.md) <br>
- [AK Configuration Guide](references/capabilities/configure.md) <br>
- [Skill Telemetry Notes](references/skill埋点说明.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/1688-common-cha88-bidding-base) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses with a human-readable markdown field] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are formatted as markdown tables; command failures return JSON with a markdown error message.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
