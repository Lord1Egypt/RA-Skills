## Description:

Helps agents use Codex CLI with GPT-5-family models to run coding tasks non-interactively, including hands-off execution, worktree setup, monitoring, review, and PR workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to delegate coding tasks to Codex CLI, run long-lived implementation sessions, monitor outputs, and manage pull-request workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports suspicious guidance because the skill recommends unsandboxed no-approval Codex runs.

Mitigation: Use the skill only in a disposable, isolated environment with no production credentials; prefer read-only or workspace-write modes and avoid the dangerous bypass flag unless isolation is in place.

Risk: The security scan reports unsafe shell examples that could execute unintended commands or push repository changes.

Mitigation: Review prompts, quoted strings, paths, and command arguments before automation, and require manual review before commits, pushes, PR comments, or cleanup.

## Reference(s):

- [ClawHub Codex Skill release](https://clawhub.ai/feiskyer/skills/codex-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task prompts, CLI flags, tmux workflow steps, monitoring commands, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
