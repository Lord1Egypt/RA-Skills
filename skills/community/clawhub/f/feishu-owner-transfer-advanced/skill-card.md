## Description:

Helps authorized users transfer ownership of Feishu Docs, Sheets, Bitable, Mindnote, files, and Wiki-linked documents using lark-cli or Python requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and administrators use this skill to prepare commands or scripts that transfer Feishu document ownership to a target user. It supports single-file, root-folder batch, and Wiki-space document transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can transfer broad sets of Feishu documents when run with an authenticated lark-cli account.

Mitigation: Use the documented dry-run/list mode first, verify each target and current owner, and limit batch or Wiki-space transfers to authorized scopes.

Risk: The documented human-owner skipping behavior is not consistent across every mode.

Mitigation: Do not rely on automatic skipping alone; explicitly review target documents and use owner filters where available before executing transfers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/feishu-owner-transfer-advanced)
- [ClawHub publisher profile](https://clawhub.ai/user/freedompixels)
- [Feishu transfer ownership API endpoint](https://open.feishu.cn/open-apis/drive/permission/member/transfer)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that change Feishu document ownership when executed with an authenticated lark-cli account or API token.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
