## Description:

Operate devopsellence solo/shared deployments, nodes, secrets, logs, diagnostics, lifecycle hooks, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elvinefendi](https://clawhub.ai/user/elvinefendi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate devopsellence deployments, including solo or shared workspace setup, deployment checks, secrets, node management, diagnostics, lifecycle hooks, rollback, and cleanup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider tokens and application secrets can be exposed if passed directly on the command line or repeated in chat.

Mitigation: Prefer stdin-based secret and provider-token examples, keep secret values out of logs and chat output, and avoid the --token form for real secrets.

Risk: Deploy, detach, remove, uninstall, and cleanup commands can affect live infrastructure.

Mitigation: Verify the selected mode, target node, and environment before deployment or removal actions, and run cleanup commands only when the user intends to detach, uninstall, and remove that node.

Risk: Unsupported or missing CLI schema versions can make structured command output unreliable for high-risk decisions.

Mitigation: Check schema_version when present; if unsupported, summarize the structured output and ask for updated docs or guidance before making high-risk changes.

## Reference(s):

- [devopsellence homepage](https://www.devopsellence.com)
- [ClawHub skill page](https://clawhub.ai/elvinefendi/skills/devopsellence)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill asks agents to treat devopsellence CLI stdout as structured JSON or newline-delimited JSON when available and to keep secret values out of logs and chat output.]

## Skill Version(s):

0.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
