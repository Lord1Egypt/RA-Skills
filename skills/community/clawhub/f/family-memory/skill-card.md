## Description:

Helps agents store, recall, and search family-related notes using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to remember family dates, notes, and coordination context across conversations. It is most relevant when family-related context should be recalled or saved through BlueColumn persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Family information is sent to and stored in BlueColumn persistent memory without clear per-write confirmation or documented limits.

Mitigation: Review each memory before storing it, avoid unnecessary details about children or sensitive schedules, and confirm how saved memories can be inspected, corrected, or deleted.

Risk: The skill requires a live BlueColumn API key for the external memory service.

Mitigation: Store the API key only in the platform secret store and do not paste it into prompts, logs, or shared files.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)
- [ClawHub skill page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/family-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends family-memory text to an external persistent memory service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
