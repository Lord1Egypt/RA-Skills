## Description:

Guides root-level ALab home administration, including bootstrap, credential management, project initialization and handoff, SkyDiscover catalog lifecycle, cleanup, audit inspection, and local dashboard use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bebetterest](https://clawhub.ai/user/bebetterest)

### License/Terms of Use:

MIT-0

## Use Case:

External developers or ALab administrators use this skill to perform root-scoped ALab home setup and maintenance, manage credentials and catalogs, initialize projects, inspect audit events, and hand off lower-layer work with least-privilege credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides high-impact root administration, including credential rotation, key revocation, project removal, catalog removal, cache pruning, and backup pruning.

Mitigation: Use root authority only for root-scoped tasks, prefer dry-runs where available, and require exact confirmations before destructive removal commands.

Risk: Root keys, project admin keys, and dashboard token URLs could be exposed in prompts, logs, commits, screenshots, reports, or shared transcripts.

Mitigation: Pass credentials through stdin, ignored secret files, private environment variables, or approved secret stores; do not share dashboard token URLs or raw keys.

Risk: Delegating root or project credentials to the wrong layer could broaden access beyond the task scope.

Mitigation: Keep root keys in root-admin sessions, pass project admin keys only to project-level sessions, and give experiment workers only worktree or inspection tokens for their exact checkout.

## Reference(s):

- [ALab Global Admin Commands](references/commands.md)
- [ALab Global Admin Commands (Chinese)](references/commands_cn.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Root-level administrative guidance; generated secrets and dashboard token URLs should not be included in shared output.]

## Skill Version(s):

0.1.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
