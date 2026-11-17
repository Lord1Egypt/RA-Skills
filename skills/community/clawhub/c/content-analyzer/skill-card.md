## Description:

Analyze Xiaohongshu (小红书) notes and Douyin (抖音) videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dizhu](https://clawhub.ai/user/dizhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze Xiaohongshu notes, Douyin videos, and creator profiles. It summarizes content, interprets engagement metrics, identifies viral patterns, and suggests actionable content improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script and makes outbound network requests to TikHub.

Mitigation: Review the script before installation, disclose third-party data flow to users, and run it only in environments where outbound TikHub requests are acceptable.

Risk: Unsafe URL handling and redirect behavior could let untrusted links trigger broader local or network access than users expect.

Mitigation: Use strict URL and redirect validation before execution and limit accepted inputs to the documented Xiaohongshu and Douyin URL patterns.

Risk: Network configuration changes may bypass expected proxy behavior.

Mitigation: Review or modify the script so it respects configured proxy policies in the deployment environment.

## Reference(s):

- [Content Analyzer Skill Page](https://clawhub.ai/dizhu/skills/content-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis based on JSON returned by the local analysis script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-post outputs include summaries, engagement interpretation, and takeaways; profile outputs include creator positioning, strategy patterns, viral patterns, and recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
