## Description:

Use when an agent needs Dreamina image or video generation through the dreamina CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mr-j-j](https://clawhub.ai/user/mr-j-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Dreamina image and video generation through a local CLI, including session checks, credit checks, task submission, asynchronous result queries, and saved task review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation commands may consume Dreamina account credits.

Mitigation: Review commands before paid submissions and check account credit before running real generation tasks.

Risk: The CLI may reuse an existing Dreamina login session.

Mitigation: Install and use the skill only when the agent is expected to access the local Dreamina CLI and the associated Dreamina account.

Risk: Asynchronous generation can be mistaken for completion at submit time.

Mitigation: Track the submit ID and query the final task result before treating generated media as complete.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to inspect CLI help before use and to track submit IDs and final task status for asynchronous generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
