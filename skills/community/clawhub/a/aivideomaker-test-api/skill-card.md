## Description: <br>
Executes AIVideoMaker API workflows for text-to-video and image-to-video generation, including task creation, status polling, task details retrieval, and cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rainlin10](https://clawhub.ai/user/rainlin10) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to create AIVideoMaker video generation tasks, poll progress, retrieve details, and cancel submitted tasks through a scriptable Node.js workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an AIVideoMaker API key and sends generation task data to AIVideoMaker. <br>
Mitigation: Use a dedicated or easily rotated API key, and avoid sending sensitive prompts or images unless you trust the provider. <br>
Risk: Generation and cancellation requests can consume credits or change task state. <br>
Mitigation: Review the model, duration, payload, and task ID before allowing create or cancel operations. <br>
Risk: Polling task status too frequently can trigger rate limits. <br>
Mitigation: Use the built-in backoff behavior, honor Retry-After responses, and lower polling frequency when needed. <br>


## Reference(s): <br>
- [AIVideoMaker API Reference](artifact/references/api-reference.md) <br>
- [Usage Examples](artifact/references/examples.md) <br>
- [AIVideoMaker](https://aivideomaker.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/rainlin10/aivideomaker-test-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON responses with optional shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Normalized status, taskId, data, errorCode, errorMessage, retryAfter, and suggestions fields for automation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact files declare 1.0.12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
