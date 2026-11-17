## Description:

Analyze and archive low-value memory notes in an OpenClaw workspace to reduce context bloat and improve responsiveness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[irideas](https://clawhub.ai/user/irideas)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to inspect workspace memory notes, plan cleanup, and archive low-value or older notes after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional JSON output path may execute attacker-controlled JavaScript when workspace paths or memory filenames are untrusted.

Mitigation: Avoid --json in untrusted workspaces or memory trees until the JSON generation is reviewed and hardened.

Risk: Archive mode moves memory files within the workspace and may overwrite archived files with duplicate basenames.

Mitigation: Run plan or archive --dry-run first, review the candidate list, and only proceed after explicit confirmation.

## Reference(s):

- [Context Cleanup policy](artifact/references/policy.md)
- [ClawHub skill page](https://clawhub.ai/irideas/skills/context-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text, with optional JSON output from analyze and plan modes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce cleanup analysis, archive plans, dry-run output, and confirmation prompts.]

## Skill Version(s):

0.3.0 (source: server release metadata; artifact metadata and changelog report 0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
