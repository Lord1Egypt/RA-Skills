## Description:

AI Tool Extension for Feishu API - A progressively extensible skill that enables AI tools (OpenClaw, Claude Code, etc.) to leverage Feishu capabilities on-demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soraclub](https://clawhub.ai/user/soraclub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure Feishu app authentication, run existing Feishu API helper scripts, and add new Feishu API scripts only when a task requires them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Feishu app credentials and caches tenant access tokens locally.

Mitigation: Use a test Feishu app with minimal scopes, keep scripts/env/app.json and token_cache.json private with strict local permissions, and avoid logging token output.

Risk: The skill instructs agents to create and run new Feishu API scripts, including potentially destructive send, update, delete, admin, or bulk operations.

Mitigation: Review new scripts before use and require explicit human confirmation before any destructive, administrative, or bulk data operation.

Risk: Feishu API calls can expose workspace data such as group membership.

Mitigation: Use least-privilege Feishu app scopes, avoid production groups until scripts are reviewed, and treat returned member lists as sensitive data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/soraclub/skills/feishu-master)
- [Publisher Profile](https://clawhub.ai/user/soraclub)
- [Feishu API Documentation Reference](references/README.md)
- [Feishu API Summary](references/feishu_api.md)
- [Feishu API Documentation URLs](references/doc_urls.txt)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Feishu Server API Documentation](https://open.feishu.cn/document/server-docs/)
- [Tenant Access Token API](https://open.feishu.cn/document/server-docs/authentication-management/access-token/tenant_access_token)
- [Get Group Member List API](https://open.feishu.cn/document/server-docs/im-v1/group-group/get_group_member_list)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python examples; included scripts return JSON from Feishu APIs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Feishu app credentials and may create or update helper scripts and script-index metadata when extending API coverage.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
