## Description:

Configures opencode.ai free AI models in WorkBuddy without an API key and helps keep the local model configuration current.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pinke](https://clawhub.ai/user/pinke)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users and developers use this skill to discover opencode.ai free model IDs and add or update those models in the local WorkBuddy model configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater can modify WorkBuddy model configuration and may overwrite a damaged config without backup.

Mitigation: Back up ~/.workbuddy/models.json before running the updater, run it interactively, and decline unexpected changes.

Risk: Installing from an unpinned remote branch can expose users to publisher or repository changes after review.

Mitigation: Install only from trusted publisher sources and prefer a pinned release or commit when available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pinke/skills/free-buddy-skills)
- [opencode.ai models endpoint](https://opencode.ai/zen/v1/models)
- [opencode.ai chat completions endpoint](https://opencode.ai/zen/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and an optional Python updater script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch model metadata from opencode.ai and update ~/.workbuddy/models.json after user confirmation.]

## Skill Version(s):

2.3.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
