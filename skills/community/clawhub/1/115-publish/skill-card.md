## Description:

Manages 115 cloud-drive accounts through QR login, file browsing, search, share saving, offline downloads, smart organization, storage queries, and cleanup advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sukris](https://clawhub.ai/user/sukris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage 115 cloud-drive files through an agent, including login, browsing, search, share transfer, offline download, organization, and storage cleanup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores reusable 115 account session cookies locally.

Mitigation: Install only in a trusted local account and workspace, and review or patch credential handling before use.

Risk: The skill can browse account metadata, create remote download tasks, move files, and perform delete or clear operations.

Mitigation: Require explicit user confirmation for downloads, organization, deletion, and recycle-bin clearing.

Risk: The security verdict is suspicious because account access and state-changing file actions have consent and security gaps.

Mitigation: Perform manual review before installation and treat the skill as having broad access to the connected 115 account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sukris/skills/115-publish)
- [115 web service](https://115.com/)
- [115 web API](https://webapi.115.com)
- [115 passport API](https://passportapi.115.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and short text responses with account status, file lists, search results, task results, progress summaries, and cleanup recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include QR login image output and concise progress or confirmation prompts for account and file operations.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
