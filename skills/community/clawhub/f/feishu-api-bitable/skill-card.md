## Description:

Feishu Bitable API helps agents create, read, update, and delete Feishu Bitable tables, records, fields, and views through a Node.js CLI/API client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevenlikewatermelon](https://clawhub.ai/user/stevenlikewatermelon)

### License/Terms of Use:

MIT

## Use Case:

Developers and operations teams use this skill to automate Feishu Bitable workflows, including table setup, record CRUD, batch imports, field inspection, and view listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete live Feishu Bitable business data.

Mitigation: Use a least-privilege Feishu app, test on non-production tables first, and confirm app, table, and record IDs before write or delete operations.

Risk: Credentials and @file inputs can expose sensitive local data if handled carelessly.

Mitigation: Keep credentials out of source control and logs, and avoid passing @file paths to sensitive local files.

Risk: Configurable request destinations can send authenticated requests to unintended endpoints.

Mitigation: Do not let untrusted input configure the API baseURL.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stevenlikewatermelon/skills/feishu-api-bitable)
- [Publisher profile](https://clawhub.ai/user/stevenlikewatermelon)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu Bitable API endpoint family](https://open.feishu.cn/open-apis/bitable/v1)
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Feishu app credentials through FEISHU_APP_ID and FEISHU_APP_SECRET or FEISHU_APP_SECRET_PATH.]

## Skill Version(s):

1.0.0 (source: server release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
