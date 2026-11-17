## Description:

Manage contacts, companies, products, tags, documents, brands, automations, team members, organization data, block plugin records, and operation plugin records on an erxes instance through GraphQL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erxes](https://clawhub.ai/user/erxes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to authenticate to an erxes gateway and manage CRM, product, brand, automation, team, block, and operation records through GraphQL. It supports read, search, group, and summarize flows, plus guarded write and delete workflows that require record identification and confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill assumes owner-level access and can perform destructive or state-changing GraphQL operations.

Mitigation: Install only in trusted erxes environments and require explicit confirmation for deletes, transfers, publishes, contract or invoice changes, member administration, and automation changes.

Risk: Runtime ERXES_BASE_URL values determine where OAuth and GraphQL requests are sent.

Mitigation: Use only trusted HTTPS erxes gateway URLs, avoid untrusted ERXES_BASE_URL values, and verify the browser approval origin before granting access.

Risk: Authentication returns access and refresh tokens for the current erxes session.

Mitigation: Keep tokens in memory for the current task and never print or persist raw tokens, session JSON, or authorization headers.

## Reference(s):

- [erxes Skill page](https://clawhub.ai/erxes/skills/erxes-skill)
- [erxes skill definition](artifact/SKILL.md)
- [erxes quick login reference](artifact/erxes-app-token-auth.md)
- [erxes GraphQL API reference](artifact/erxes-graphql-api.md)
- [block_api SaaS workflow reference](artifact/block-api.md)
- [operation_api SaaS workflow reference](artifact/operation-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, GraphQL snippets, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use browser-based OAuth approval and authenticated GraphQL calls; session tokens are kept in memory for the current task.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
