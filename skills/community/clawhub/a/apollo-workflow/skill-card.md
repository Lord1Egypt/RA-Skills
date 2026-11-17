## Description:

Apollo Workflow is a Chinese-language coding workflow that turns ideas into usable code through gated phases for brainstorming, planning, subagent development, debugging, and branch finishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to structure feature development, bug fixing, implementation planning, and branch completion with hard phase gates, TDD, subagent review, and workflow state tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad activation triggers and can steer normal coding requests into a stateful workflow.

Mitigation: Review the trigger behavior before installation and enable it only where a Chinese-language gated coding workflow is desired.

Risk: Bundled shell scripts accept task IDs, result paths, or phase names that the security evidence flags as unsafe until heredoc injection issues are fixed.

Mitigation: Do not run the helper scripts with untrusted inputs; inspect or patch the scripts before operational use.

Risk: Workflow helpers write state under a fixed global workflow directory.

Mitigation: Prefer a project-local workflow directory or isolate the runtime environment before using the scripts.

Risk: The testing reference recommends a --break-system-packages install command.

Mitigation: Use a virtual environment or other isolated Python environment instead of modifying a shared or system Python installation.

## Reference(s):

- [Apollo Workflow Skill Page](https://clawhub.ai/nic-yuan/skills/apollo-workflow)
- [Publisher Profile](https://clawhub.ai/user/nic-yuan)
- [Brainstorming Reference](references/brainstorming.md)
- [Writing Plans Reference](references/writing-plans.md)
- [Subagent-Driven Development Reference](references/subagent-development.md)
- [Systematic Debugging Reference](references/systematic-debugging.md)
- [Finishing a Development Branch Reference](references/finishing-branch.md)
- [Test-Driven Development Reference](references/tdd.md)
- [Testing Reference](references/testing.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON gate/state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow instructions; may create or update plans, tests, commits, workflow state, gate files, and task result files.]

## Skill Version(s):

3.0.1 (source: server release evidence; artifact frontmatter shows 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
