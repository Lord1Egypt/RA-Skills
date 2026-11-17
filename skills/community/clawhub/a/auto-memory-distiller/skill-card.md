## Description:

Auto Memory Distiller converts OpenClaw conversation history into structured, themed Markdown memory cards with source traceability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mashirops](https://clawhub.ai/user/mashirops)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers can use this skill to incrementally distill long-running conversation logs into persistent Markdown knowledge cards organized by topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation history may be processed and sent to Google's Gemini API.

Mitigation: Enable the skill only for sessions that users explicitly approve and add local secret redaction before external processing.

Risk: Persistent memory cards may be written without clear review controls.

Mitigation: Add review steps or allowlists before memory writes are accepted as long-term knowledge.

Risk: Automatic cron or heartbeat execution can process broad local history silently.

Mitigation: Avoid scheduled execution until opt-in, dependency pinning, and review controls are in place.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown files with configuration notes and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates topic memory cards with source file and line pointers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
