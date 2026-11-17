## Description:

Subscribes to Douyin account IDs, fetches recent works daily, and returns grouped Markdown tables plus generated HTML reports with engagement metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators, short-video creators, brands, and MCNs use this skill to monitor selected Douyin accounts, review recent works, and receive daily content digests for competitive or trend analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates recurring daily monitoring tasks for subscribed Douyin accounts.

Mitigation: Review scheduled tasks after subscription and remove accounts or tasks that are no longer intended.

Risk: Tracked Douyin account IDs are sent to redfox.hk for data retrieval.

Mitigation: Subscribe only to account IDs the user intends to share with the RedFox service.

Risk: Subscription and failure state may be stored locally under ~/.qoder.

Mitigation: Inspect or remove ~/.qoder/douyin_subscriptions.json and ~/.qoder/douyin_subscribe_failures.json when changing subscriptions or uninstalling the skill.

Risk: API keys can be exposed if passed on the command line or written into prompts, logs, or reports.

Mitigation: Prefer REDFOX_API_KEY from a protected environment or secret store and avoid using --api-key.

Risk: Generated HTML reports are opened automatically and the security guidance notes an unresolved report escaping issue.

Mitigation: Treat generated reports as untrusted content and avoid opening them automatically until the escaping issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/douyin-subscribe)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [Douyin work-by-account API test parameters](artifact/references/test_api_params.json)
- [Douyin ID example image](https://lyy.redfox.hk/page/ljq.png)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown tables, generated HTML report files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY and a list of Douyin account IDs; generated reports are saved under a report directory or a caller-provided HTML path.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
