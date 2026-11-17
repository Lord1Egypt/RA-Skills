## Description:

Use Cursor safely across editor, CLI, rules, background agents, Bugbot, and MCP workflows with repo-aware context and reviewable execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate Cursor across editor, CLI, rules, background agents, Bugbot, MCP, indexing, and privacy-sensitive workflows while keeping execution scope and review expectations explicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cursor workflows can send selected prompts, code context, diffs, indexing data, and GitHub workflow metadata to Cursor or GitHub services.

Mitigation: Confirm the active Cursor surface and data flow before use, and review privacy, indexing, GitHub, Background Agent, Bugbot, and MCP boundaries for the target repository.

Risk: Remote Background Agents, Bugbot, remote MCP, and non-interactive cursor-agent runs can widen execution scope or operate outside local interactive review.

Mitigation: Require explicit approval for those modes, pin the repository and objective, define allowed files and verification steps, and inspect outputs before merging or applying changes.

Risk: Cursor ignore and indexing controls reduce exposure but are not complete secret barriers.

Mitigation: Keep secrets and production credentials outside accessible repository paths and rely on repository, filesystem, and integration boundaries for data that must never be exposed.

## Reference(s):

- [ClawHub Cursor skill page](https://clawhub.ai/ivangdavila/skills/cursor)
- [Cursor product site](https://cursor.com/)
- [Cursor documentation](https://docs.cursor.com/)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create durable Cursor operating notes under ~/cursor/ after user consent.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
