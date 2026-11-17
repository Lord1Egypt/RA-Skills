## Description:

Auto Publish helps agents prepare and run multi-platform content publishing workflows for Douyin, Xiaohongshu, Bilibili, YouTube, and related video channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nh5gntnf78-oss](https://clawhub.ai/user/nh5gntnf78-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations teams use this skill to configure publishing credentials, generate tags and recommended publish times, queue single or batch posts, and review simulated tracking outputs for multi-platform content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to place platform credentials in scripts/config.json.

Mitigation: Use test accounts or environment-specific throwaway credentials, keep real secrets out of config files, and remove credentials before packaging or sharing archives.

Risk: Publishing and analytics outputs may appear successful even when they are simulated.

Mitigation: Verify posts and metrics directly in the official platform dashboards before treating reported URLs, counts, or revenue estimates as real.

Risk: Packaging can include local files from the skill directory.

Mitigation: Review archive contents before distribution and exclude logs, generated result files, credentials, or private media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nh5gntnf78-oss/skills/auto-publish)
- [Douyin Open Platform](https://open.douyin.com/)
- [Xiaohongshu Open Platform](https://open.xiaohongshu.com/)
- [Bilibili Open Platform](https://open.bilibili.com/)
- [Google Cloud Console](https://console.cloud.google.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON files, Guidance]

**Output Format:** [Markdown instructions with Python and shell examples, plus JSON configuration and result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON outputs such as publish_results.json, generated tag files, tracking reports, logs, or .skill archives.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
