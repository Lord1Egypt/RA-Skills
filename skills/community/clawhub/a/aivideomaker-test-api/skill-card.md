## Description:

Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task details retrieval, and cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rainlin10](https://clawhub.ai/user/rainlin10)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to create AIVideoMaker video generation tasks, poll status, retrieve task details, and cancel submitted tasks through a Node.js command workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, generated outputs, and task history are tied to the configured AIVideoMaker API key.

Mitigation: Install and use only if you trust AIVideoMaker with that data; avoid shared or high-privilege keys and rotate keys regularly.

Risk: Task IDs supplied from untrusted text can affect task lookup or cancellation requests.

Mitigation: Use task IDs from trusted workflow outputs and add stricter taskId validation before production automation.

Risk: The security evidence flags under-scoped request construction for production use.

Mitigation: Review and tighten URL encoding and request construction before using the skill in production automation.

## Reference(s):

- [AIVideoMaker API Reference](references/api-reference.md)
- [Usage Examples](references/examples.md)
- [AIVideoMaker](https://aivideomaker.ai)
- [ClawHub skill page](https://clawhub.ai/rainlin10/skills/aivideomaker-test-api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Structured JSON command output with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized fields include ok, status, taskId, data, errorCode, errorMessage, retryAfter, httpStatus, and timestamp.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter, manifest, and package.json report 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
