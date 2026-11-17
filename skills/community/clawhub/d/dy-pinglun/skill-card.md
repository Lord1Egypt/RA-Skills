## Description:

Collects comments and replies from public Douyin videos in user-approved steps, with results available as CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuiyunhai](https://clawhub.ai/user/cuiyunhai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts collect public Douyin video comments and replies for audience feedback and sentiment review, then inspect results or export them as CSV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default connection can send saved credentials and collected comments without transport encryption.

Mitigation: Trust the account service and configure a verified HTTPS base URL before logging in or collecting comments.

Risk: Paid collection steps are not protected by executable confirmation enforcement.

Mitigation: Confirm the estimated credit cost with the user before starting and ask again before each additional paid step; monitor the balance.

Risk: Local token configuration and exported comments may expose sensitive information.

Mitigation: Avoid shared or legacy XHS config files; restrict access to token configuration and exported CSVs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cuiyunhai/skills/dy-comments)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Markdown guidance, JSON command responses, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Incremental comments and replies include nicknames, content, timestamps, likes, and IP locations; CSV exports contain collected comment data.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
