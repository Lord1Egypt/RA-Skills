## Description:

Delegate coding tasks to Blackbox AI CLI agent, a multi-model agent with a built-in judge that runs tasks through multiple LLMs and picks the best result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agungprabowo123](https://clawhub.ai/user/agungprabowo123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to delegate software engineering tasks to Blackbox CLI, including one-shot tasks, longer background runs, PR reviews, multi-model judging, and CLI session management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates work to a mutable third-party CLI with broad coding-agent authority over a project workspace.

Mitigation: Use a pinned, reviewed Blackbox CLI version in an isolated environment and review all file changes before merging or running them.

Risk: Auto-approval behavior can allow unwanted model actions or file changes on real repositories.

Mitigation: Avoid `--yolo` on real repositories and keep long-running sessions monitored.

Risk: Prompts, project code, or secrets may be sent to Blackbox or configured model providers.

Mitigation: Remove secrets before delegation and assume submitted prompts and code may leave the local environment.

Risk: Global install commands can alter the host environment or install unreviewed code.

Mitigation: Do not run install commands with elevated privileges; install only reviewed versions in disposable or isolated environments.

## Reference(s):

- [Blackbox AI](https://www.blackbox.ai/)
- [Blackbox CLI Repository](https://github.com/blackboxaicode/cli)
- [Blackbox API Dashboard](https://app.blackbox.ai/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/agungprabowo123/skills/blackbox-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate interactive or background terminal sessions when used by an agent with terminal access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
