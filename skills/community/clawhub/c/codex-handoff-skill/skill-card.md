## Description:

Offload finalized coding plans to Codex CLI for automated execution, with Claude Code supervising and judging the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philipbankier](https://clawhub.ai/user/philipbankier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to hand a finalized coding plan to Codex CLI, supervise iterative execution, review diffs and tests, and decide whether additional correction loops are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Codex CLI may modify the current repository automatically in full-auto workspace-write mode.

Mitigation: Use the skill only on trusted repositories, review the resulting diff before keeping changes, and run the relevant tests before finalizing.

Risk: Project context included in the handoff may be exposed to the Codex provider.

Mitigation: Avoid handing off sensitive repository contents or secrets, and review prompts for unnecessary private context before execution.

Risk: Untrusted or weakly reviewed model arguments could change execution behavior.

Mitigation: Use only trusted model selections and avoid passing model values supplied by untrusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philipbankier/skills/codex-handoff-skill)
- [Publisher profile](https://clawhub.ai/user/philipbankier)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include completion summaries, remaining work, test results, and correction prompts for Codex CLI.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
