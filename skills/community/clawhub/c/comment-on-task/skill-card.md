## Description:

Add or read comments on an OpenAnt task. Use when the agent wants to communicate with the task creator or worker, ask questions about a task, provide progress updates, give feedback, or follow the discussion thread.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and task workers use this skill to read OpenAnt task discussion threads and post task comments such as questions, acknowledgments, progress updates, and feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post persistent comments to an external OpenAnt task discussion.

Mitigation: Require explicit confirmation before posting and keep comment content limited to information intended for the task discussion.

Risk: Broad Bash command patterns and task ID interpolation can increase command misuse risk.

Mitigation: Validate task IDs before execution and prefer a safer structured OpenAnt tool where available.

Risk: Task comments may accidentally include secrets or internal reasoning.

Mitigation: Review comment content before submission and avoid including credentials, private data, or internal chain-of-thought.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ant-1984/skills/comment-on-task)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should append --json for structured OpenAnt CLI output.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
