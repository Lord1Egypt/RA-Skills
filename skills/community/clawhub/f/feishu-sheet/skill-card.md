## Description:

Enables an agent to create, read, edit, style, merge, search, and manage Feishu Sheets using configured Feishu app credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siyiding](https://clawhub.ai/user/siyiding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an OpenClaw agent automate Feishu spreadsheet workflows, including report creation, data reads and writes, formatting, worksheet management, images, and find-and-replace actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted image URL fetching may retrieve untrusted remote content.

Mitigation: Avoid float_image_url unless URL fetching is sandboxed or restricted to an allowlist.

Risk: Local image path handling can expose unexpected files when untrusted paths are supplied.

Mitigation: Accept only explicit, trusted image paths from the user before insert_image or float_image operations.

Risk: Delete and overwrite commands can permanently alter Feishu spreadsheet content.

Mitigation: Require explicit confirmation before delete, overwrite, merge, or replacement operations.

Risk: Tenant access tokens are cached under the temporary directory.

Mitigation: Harden token cache storage before shared-system use and prefer per-user isolated runtime environments.

Risk: Broad Feishu app permissions increase blast radius if credentials are misused.

Mitigation: Use a minimal-permission Feishu app with only the spreadsheet permissions required for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siyiding/skills/feishu-sheet)
- [Skill metadata homepage](https://clawhub.ai/skills/feishu-sheet)
- [Feishu Open API endpoint](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown guidance with inline shell commands; command results are JSON from the Feishu Open API wrapper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, bash, Feishu app credentials, and sheets:spreadsheet permission.]

## Skill Version(s):

1.2.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
