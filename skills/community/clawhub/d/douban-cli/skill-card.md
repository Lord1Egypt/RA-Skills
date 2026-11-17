## Description:

Maps explicit Douban-sourced movie, TV, book, collection, account, batch, and export requests to appropriate douban CLI commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marvae](https://clawhub.ai/user/marvae)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly want Douban as the source, or explicitly want the douban CLI, for movie, TV, book, collection, account-management, batch-operation, or export workflows. It helps the agent choose commands, parameters, paging behavior, confirmation points, and privacy handling for douban CLI use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unpinned third-party executable that may change after review.

Mitigation: Install only a trusted, pinned, reviewed version of @marvae24/douban-cli before use.

Risk: Login, browser-profile extraction, and cookie import can expose Douban session cookies.

Mitigation: Do not paste cookies into chat or logs; run cookie import locally, avoid uploading cookie files, and use logout or a restricted profile/account when finished.

Risk: Account write actions and exports can change or disclose personal account data.

Mitigation: Require explicit confirmation before follow, unfollow, rating, comment, review, mark, unmark, login, or export commands, and write exports only to user-specified paths.

## Reference(s):

- [Douban CLI homepage](https://github.com/Marvae/douban-cli)
- [ClawHub skill page](https://clawhub.ai/marvae/skills/douban-cli)
- [ClawHub publisher profile](https://clawhub.ai/user/marvae)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file-format notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command confirmations, pagination guidance, JSON/stdout notes, and privacy warnings for login, cookies, account writes, and exports.]

## Skill Version(s):

0.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
