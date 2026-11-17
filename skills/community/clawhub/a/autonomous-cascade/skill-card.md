## Description:

Guides an agent through a structured Plan, Act, and Evaluate loop for multi-step autonomous tasks until the goal is reached, blocked, or budget limits are hit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hupmann86-cell](https://clawhub.ai/user/hupmann86-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to structure unattended multi-step agent work with explicit planning, evaluation, stop conditions, and budget controls. It is intended for tasks such as diagnostics, workspace updates, and iterative optimization where the agent can proceed without repeated user prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway diagnostic example can cause broad process termination by forcing all Node.js processes to stop without confirming they belong to the target gateway.

Mitigation: Before any forced termination, identify the specific PID bound to the target port, verify it is the intended gateway process, attempt a graceful stop first, and ask the user before force-killing a process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hupmann86-cell/skills/autonomous-cascade)
- [ClawHub publisher profile](https://clawhub.ai/user/hupmann86-cell)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with structured loop templates and inline shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes round limits, budget limits, risk posture labels, and halt conditions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
