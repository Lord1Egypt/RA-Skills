## Description:

Automatically fetches Bilibili sitewide ranking video data with detailed video statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangjinghua0127](https://clawhub.ai/user/yangjinghua0127)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve the current Bilibili sitewide Top 50 ranking and save public video statistics for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Bilibili's public API when invoked and can create or overwrite workspace/scripts/bilibili-hot.json and workspace/scripts/bilibili-hot.txt.

Mitigation: Run it only when external API access and these workspace file outputs are acceptable; review generated ranking files before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangjinghua0127/skills/bilibili-hot)
- [Bilibili ranking API](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [Console text plus saved JSON and plain-text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 50 sitewide ranking entries and writes bilibili-hot.json and bilibili-hot.txt under workspace/scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
