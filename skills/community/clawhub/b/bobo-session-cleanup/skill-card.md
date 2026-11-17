## Description:

Deprecated OpenClaw session cleanup helper for scanning orphan .jsonl files and stale sessions, with migration recommended to session-cleanup-pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irideas](https://clawhub.ai/user/irideas)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this legacy skill to inspect local OpenClaw session storage, identify orphan session files and stale sessions, and prepare a cleanup plan that requires user confirmation before action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects local OpenClaw session files and can lead to deleting session data after approval.

Mitigation: Review the scan summary first, prefer archive or move operations, and proceed with deletion only after explicit confirmation.

Risk: Hard-delete commands can remove the wrong file if filenames are not taken directly from trusted scan output or are not safely quoted.

Mitigation: Use filenames from the scan output, quote paths carefully, and perform a second confirmation before permanent deletion.

Risk: Recent or active sessions could be disrupted by overly broad cleanup.

Mitigation: Keep the default 72-hour protection window and never delete the protected agent:main:main session.

## Reference(s):

- [Cleanup Policy](references/policy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON scan output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scan script emits JSON summarizing registered sessions, on-disk .jsonl files, orphan files, stale sessions, protected sessions, and estimated reclaimable bytes.]

## Skill Version(s):

0.2.1 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
