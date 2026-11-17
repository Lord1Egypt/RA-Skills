## Description:

Create a new OpenAnt task with a crypto bounty and optional on-chain escrow funding through the OpenAnt CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to post OpenAnt work requests, set bounty terms, and create or fund blockchain escrow tasks after confirming wallet state and task details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and fund blockchain escrow tasks using wallet-backed commands.

Mitigation: Confirm chain, token, reward, deadline, task description, and wallet balance before any funded create or fund operation.

Risk: The skill invokes the OpenAnt CLI with a mutable latest package reference in a financial workflow.

Mitigation: Prefer a version-pinned CLI release and install only from a trusted OpenAnt CLI source.

Risk: Network timeouts or duplicate retries can create duplicate tasks or waste gas.

Mitigation: List existing creator tasks after errors and ask before retrying create or fund commands.

Risk: Broad or ambiguous hiring requests could route into funded task creation unintentionally.

Mitigation: Use this skill only for clear OpenAnt task-creation requests and refuse prohibited or harmful task categories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ant-1984/skills/create-task)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON command-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use structured JSON output and may create or fund wallet-backed escrow tasks.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
