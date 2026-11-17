## Description:

Dispatch coding tasks to the local OpenAI Codex CLI with background execution, status polling, and answerable clarifying questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeperl](https://clawhub.ai/user/abeperl)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to delegate script building, code edits, refactors, and multi-step coding work from OpenClaw to a local Codex CLI session while keeping status polling and clarifying-question handling available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches local Codex jobs with broad coding-agent authority in the selected project directory.

Mitigation: Install only when this delegation behavior is intended, and prefer running jobs in a contained workspace.

Risk: Server security evidence reports local path and storage safety gaps.

Mitigation: Use simple safe task IDs, avoid secrets in prompts, inspect or clean ~/.codex-bridge regularly, and wait for task-ID validation and restrictive file permissions before higher-trust use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abeperl/skills/codex-bridge)
- [Publisher profile](https://clawhub.ai/user/abeperl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands with JSON status, question, and result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the local codex CLI; bridge state is stored under ~/.codex-bridge/tasks.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
