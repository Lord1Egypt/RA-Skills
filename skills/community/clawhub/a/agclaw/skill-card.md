## Description:

AppGrowing intelligent ad creative analysis assistant with Strategy Exploration and Inspiration modes for ad creative analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcloud](https://clawhub.ai/user/youcloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to analyze AppGrowing ad creative data, explore campaign strategy, and generate creative inspiration through the AppGrowing/YouCloud analysis service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and analysis requests may be sent to the external AppGrowing/YouCloud service.

Mitigation: Use the skill only for intended AppGrowing ad creative analysis and avoid sending confidential business data unless approved for that service.

Risk: The skill requires a YOUCLOUD_API_KEY and may accept API keys pasted into chat.

Mitigation: Configure YOUCLOUD_API_KEY securely as an environment variable and avoid pasting API keys into chat.

Risk: The security evidence marks the release as suspicious and recommends review before installation.

Mitigation: Review the skill and its external-service behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youcloud/skills/agclaw)
- [Publisher profile](https://clawhub.ai/user/youcloud)
- [AppGrowing homepage](https://appgrowing.cn/)
- [Usage examples](references/example.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown analysis returned from the AppGrowing/YouCloud service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ad creative summaries, strategy observations, creative scripts, and material links when returned by the service.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
