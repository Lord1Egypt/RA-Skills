## Description:

EvoMap Node Controller helps agents start, stop, configure, monitor, and troubleshoot EvoMap evolver nodes after the required environment variables are configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2233admin](https://clawhub.ai/user/2233admin)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage EvoMap node processes, including starting and stopping remote evolver loops, checking status, configuring node identifiers, and troubleshooting connection or binding issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run privileged remote SSH commands against hard-coded EvoMap servers.

Mitigation: Use it only in environments where controlling those servers is intended, replace hard-coded server and key assumptions with explicit configuration, and run through a dedicated unprivileged service account.

Risk: The skill disables SSH host-key checking and can start or stop long-running processes with weak safeguards.

Mitigation: Verify SSH host keys, require confirmation for start and stop actions, and manage the loop through a service manager instead of nohup and pkill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2233admin/skills/evomap-node-controller)
- [EvoMap Hub](https://evomap.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text status results and Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute SSH-based node management commands when invoked by an agent in an environment with the required keys and configuration.]

## Skill Version(s):

2.1.0 (source: server release evidence; package.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
