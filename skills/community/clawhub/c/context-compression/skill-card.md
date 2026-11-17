## Description:

Prevent context overflow with automatic session truncation and memory preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lifei68801](https://clawhub.ai/user/lifei68801)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to keep local agent sessions within context limits by configuring session truncation, priority preservation, fact extraction, and memory note maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic truncation can rewrite OpenClaw session history and create data-loss risk.

Mitigation: Review the scripts and configuration, test manually, keep backups of session files, and enable cron only after accepting the rewrite behavior.

Risk: Fact extraction can persist sensitive, incorrect, or injected conversation content into MEMORY.md and daily notes.

Mitigation: Audit generated memory files and daily notes regularly, and remove secrets or untrusted instructions before relying on them.

Risk: AI-assisted fact identification may route session content according to the user's OpenClaw provider configuration.

Mitigation: Leave AI-assisted extraction disabled unless provider-side handling of session content is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lifei68801/skills/context-compression)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OpenClaw session and memory files when its shell scripts are run.]

## Skill Version(s):

3.13.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
