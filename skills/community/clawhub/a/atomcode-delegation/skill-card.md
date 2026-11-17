## Description:

Delegates independent coding tasks to the AtomCode CLI in headless mode, including single-task and batch execution, monitoring, timeouts, and session continuation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate independent repository changes to AtomCode, run several bounded coding tasks in parallel, and monitor or resume them with explicit logs, timeouts, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended AtomCode runs can make repository changes without interactive review.

Mitigation: Run in a clean branch, disposable worktree, container, or low-privilege account, and review git diff before keeping changes.

Risk: Prompts and logs written to shared temporary locations may expose sensitive content.

Mitigation: Avoid putting secrets in prompts or logs, use private temporary directories instead of shared /tmp paths, and clean up task artifacts after use.

## Reference(s):

- [AtomCode CLI](https://atomgit.com/atomcode)
- [ClawHub Skill Page](https://clawhub.ai/vincentlau2046-sudo/skills/atomcode-delegation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed atomcode CLI and configured providers; guidance can launch unattended repository-modifying commands.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
