## Description:

Feishu Wiki skill for creating knowledge spaces and Wiki page nodes so teams can organize and preserve documents in Feishu knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyyao2222-eng](https://clawhub.ai/user/sunnyyao2222-eng)

### License/Terms of Use:


## Use Case:

Developers and operations teams use this skill to automate Feishu Wiki space creation, page node creation, node lookup, and node movement for structured knowledge-base management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends broad space-wide administrator access for a bot identity.

Mitigation: Use a dedicated bot identity, grant access only to the specific Feishu spaces or subtrees needed, and avoid space-wide administrator group membership unless operationally unavoidable.

Risk: The skill supports high-impact wiki reorganization actions such as creating top-level spaces, moving nodes, deleting nodes, or applying broad permissions.

Mitigation: Require human confirmation before top-level space creation, node movement, node deletion, or broad permission changes, and document how to revoke the bot's Feishu permissions after use.

## Reference(s):

- [Feishu Wiki v2 API](https://open.feishu.cn/open-apis/wiki/v2)
- [ClawHub skill page](https://clawhub.ai/sunnyyao2222-eng/skills/feishu-wiki)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with API endpoint examples and JSON payload snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Feishu tenant access tokens, Wiki space identifiers, node tokens, object tokens, and permission scopes supplied by the user or runtime environment.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
