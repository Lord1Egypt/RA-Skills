## Description:

Getnote 1.5.7 lets an agent save, search, list, update, delete, and organize a user's Get笔记 notes and knowledge bases through the Get笔记 OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackie2010](https://clawhub.ai/user/jackie2010)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an agent to Get笔记 so it can capture links, text, and images, then retrieve or organize private notes and knowledge-base content on request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private Get笔记 notes and long-lived credentials.

Mitigation: Install only if comfortable granting access to private notes, keep OAuth and API output secret, and configure GETNOTE_OWNER_ID before use in shared or group chats.

Risk: Helper scripts may be used with sensitive local paths or credential-bearing parameters.

Mitigation: Avoid sensitive local paths, review script arguments and output before sharing, and prefer ClawHub installation over raw GitHub curl installation.

Risk: The skill can write notes and may encounter API membership, quota, or rate-limit failures.

Mitigation: Review requested write actions before execution, preserve the documented owner checks, and honor API error and rate-limit guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackie2010/skills/getnote-1-5-7)
- [Get笔记 homepage](https://biji.com)
- [Get笔记 Open Platform](https://www.biji.com/openapi)
- [Get笔记 OpenAPI base URL](https://openapi.biji.com)
- [Get笔记 API details](references/api-details.md)
- [Save notes](references/save.md)
- [Semantic search](references/search.md)
- [Note list and details](references/list.md)
- [Knowledge base management](references/knowledge.md)
- [OAuth authorization configuration](references/oauth.md)
- [Tag management](references/tags.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command snippets and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to call the Get笔记 OpenAPI when configured with user credentials.]

## Skill Version(s):

1.5.7 (source: package.json); ClawHub release 1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
