## Description:

Extract and monitor Apple Notes content for workflow integration. Supports bulk extraction, real-time monitoring, and export to various formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianderrington](https://clawhub.ai/user/ianderrington)

### License/Terms of Use:


## Use Case:

Developers and operators on macOS use this skill to extract Apple Notes into structured local files and to monitor note changes for downstream workflow integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The full and auto extraction paths may install and run unpinned third-party Ruby parser code.

Mitigation: Use the simple local extraction path by default, and enable full or auto extraction only after the Ruby parser and dependencies are reviewed and pinned.

Risk: Automation and integration examples can persist or copy private notes into external systems or long-lived stores.

Mitigation: Do not enable cron, daemon, AI, Notion, Git, webhook, or remote-backup workflows until approved note scope, storage locations, retention, and deletion paths are defined.

Risk: Extracted note content may include sensitive personal or business information.

Mitigation: Review privacy filters before use, inspect output directories, and avoid exporting attachments or full-text indexes unless they are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ianderrington/skills/apple-notes-extractor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON or Markdown note exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local extraction output may include note text, metadata, attachments, and workflow export files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
