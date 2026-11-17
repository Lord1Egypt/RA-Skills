## Description:

Teaches an agent to use Feishu/Lark Bitable tools to create, read, and update records while resolving wiki and base URLs to the correct app_token before operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingzuer](https://clawhub.ai/user/lingzuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when their agent needs to manage Feishu/Lark Bitable data, especially when user input may contain wiki URLs that must be resolved before CRUD operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update live Feishu Bitable data.

Mitigation: Use a Feishu app with the narrowest practical permissions and confirm the target base, table, record, and fields before write operations.

Risk: Using a wiki node_token as an app_token can cause Bitable operations to fail.

Mitigation: Resolve Feishu wiki and base URLs with feishu_bitable_get_meta before running record or field operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingzuer/skills/feishu-bitable-crud)
- [ClawHub publisher profile](https://clawhub.ai/user/lingzuer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline tool-call examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Feishu plugin and appropriate Feishu app and resource permissions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
