## Description:

Interacts with the CNB (Cloud Native Build) Open API for code management and development collaboration tasks, including repositories, issues, pull requests, builds, organizations, members, releases, registries, and related platform data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sixther-dc](https://clawhub.ai/user/sixther-dc)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering agents use this skill to look up and operate on CNB platform resources through authenticated OpenAPI calls. It is suited for repository, issue, pull request, build, organization, member, release, registry, workspace, and security workflows where the agent should execute curl requests and summarize returned API data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a broad authenticated CNB API operator that can perform destructive repository and organization actions without clear confirmation safeguards.

Mitigation: Install with a least-privilege CNB token, prefer read-only tokens for lookup tasks, and require manual review before create, update, delete, permission, merge, build, registry, workspace, organization, or AI PR actions.

Risk: Token exposure or unintended API targeting can occur if credentials are stored broadly or the API endpoint is changed unexpectedly.

Mitigation: Avoid storing CNB_TOKEN in global shell startup files when possible, scope tokens to the task, and keep CNB_API_ENDPOINT fixed to a trusted HTTPS CNB host.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sixther-dc/skills/cnb-openapi)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Claude Code installation](docs/claudecode.md)
- [OpenClaw installation](docs/openclaw.md)
- [Node usage](docs/node.md)
- [Go usage](docs/go.md)
- [CNB API endpoint](https://api.cnb.cool)
- [CNB knowledge base documentation](https://docs.cnb.cool/zh/ai/knowledge-base.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with curl commands, configuration notes, and summarized CNB API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and CNB_TOKEN; CNB_API_ENDPOINT is optional and should remain fixed to a trusted HTTPS CNB host.]

## Skill Version(s):

1.18.9 (source: ClawHub release evidence, released 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
