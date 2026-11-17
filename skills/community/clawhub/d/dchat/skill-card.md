## Description:

Decentralized P2P bot-to-bot messaging over NKN. Send and receive text, images, audio, and files without any centralized server. Private, encrypted, serverless.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zbruceli](https://clawhub.ai/user/zbruceli)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use dchat to send and receive encrypted peer-to-peer messages and media over NKN without operating a central server. It also supports contact aliases, message history, listening bots, and address sharing for bot-to-bot or bot-to-human workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote media handling may allow writes outside the media cache or exhaust local resources.

Mitigation: Run the skill in an isolated user account or sandbox, disable or gate automatic downloads, and confirm media path validation and incoming size limits before normal use.

Risk: The skill connects to NKN and IPFS networks and creates persistent local identity, database, and media cache files.

Mitigation: Review network access before installing, restrict filesystem permissions, and treat all received media as untrusted.

Risk: Server evidence calls out sender-selected gateway behavior, dependency updates, and missing packaged wrapper/dist files as items to fix before lower-risk deployment.

Mitigation: Verify packaged runtime files, update dependencies, and constrain or review sender-selected gateway use before relying on the skill.

## Reference(s):

- [ClawHub dchat Skill Page](https://clawhub.ai/zbruceli/skills/dchat)
- [NKN Network](https://nkn.org)
- [nMobile](https://nmobile.nkn.org/)
- [dchat Desktop](https://github.com/nickytonline/dchat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with inline shell commands, CLI output text, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a persistent local NKN identity, SQLite message database, contact records, and media cache under the user's home directory.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
