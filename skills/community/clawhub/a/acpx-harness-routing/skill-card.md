## Description:

Routes ACPX harness tasks to Claude, Codex, or Gemini with guidance for one-shot runs, continuous named sessions, approvals, working directories, and timeouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaoyang78](https://clawhub.ai/user/chaoyang78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide how to delegate harness work across Claude, Codex, and Gemini. It is intended for ACPX workflows that need explicit routing rules, session continuity, approval behavior, and non-interactive execution parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs delegated agents to run with blanket approval and denied interactive prompts, which can allow unintended file or command changes.

Mitigation: Use explicit task boundaries, keep delegated workers sandboxed to the intended workspace, and review generated changes before using them on valuable repositories or sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaoyang78/skills/acpx-harness-routing)
- [Publisher profile](https://clawhub.ai/user/chaoyang78)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline text and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language routing guidance for ACPX harness task delegation.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
