## Description:

Doc Collaboration Watcher monitors Markdown collaboration documents for changes, records change history, and notifies configured OpenClaw communication channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lewistouchtech](https://clawhub.ai/user/lewistouchtech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and multi-agent teams use this skill to monitor shared Markdown documents, notify enabled collaboration channels about document changes, and maintain a lightweight change history for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real-looking ClawHub token appears in the release materials.

Mitigation: Revoke and remove the token, then republish a cleaned release before installation or distribution.

Risk: Automatic monitoring and notification can send document metadata or local paths through enabled channels.

Mitigation: Require explicit channel selection or confirmation before forwarding document metadata outside the host.

Risk: The stop command uses a broad process match for doc-watcher.py.

Mitigation: Replace broad process-kill commands with a scoped process identifier or service manager command.

Risk: Runtime dependency versions are not pinned in the artifact.

Mitigation: Pin dependencies and review updates before deploying the watcher.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lewistouchtech/skills/doc-collaboration-watcher)
- [Publisher profile](https://clawhub.ai/user/lewistouchtech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets, shell commands, notification text, and JSON change-history records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Monitors local Markdown files and may emit notifications through enabled OpenClaw channels.]

## Skill Version(s):

1.6.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
