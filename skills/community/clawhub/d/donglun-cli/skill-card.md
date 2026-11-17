## Description:

Posts, replies to, browses hot posts, and views Donglun forum posts and replies using a user-provided token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnoolteam](https://clawhub.ai/user/cnoolteam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to interact with the Donglun forum through command-line workflows for browsing posts, reading replies, and publishing posts or replies under an authorized account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post or reply under the user's Donglun account.

Mitigation: Install only for trusted agents and approve the exact post or reply text and target before publishing.

Risk: A token can be saved in plaintext config.json or supplied on the command line.

Mitigation: Prefer CNOOL_API_TOKEN or a secure secret store, avoid --save-config, and keep config.json out of shared repositories.

Risk: Using @file content can publish local file contents to the forum.

Mitigation: Review the file path and file contents before invoking post or reply commands.

Risk: High-frequency posting or replies can trigger account restrictions or violate community rules.

Mitigation: Follow Donglun community requirements and apply conservative rate limits for posting workflows.

## Reference(s):

- [Donglun Forum](https://bbs.cnool.net)
- [ClawHub skill page](https://clawhub.ai/cnoolteam/skills/donglun-cli)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local file content for post or reply bodies when content is supplied with an @file path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
