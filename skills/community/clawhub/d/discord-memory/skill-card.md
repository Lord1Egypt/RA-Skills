## Description:

Give AI agents Remember Discord conversations. using BlueColumn persistent memory. Use when an agent operates in Discord servers and needs continuity; when the user wants to store, recall, or search discord memory context. Requires a BlueColumn API key (bc_live_*).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents operating in Discord servers use this skill to recall, store, and search conversation summaries for continuity across interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord conversation summaries may be stored in an external persistent memory service without clear consent, scope, or retention guidance.

Mitigation: Install only for Discord servers or workspaces that explicitly authorize this storage, and avoid private channels, direct messages, secrets, personal data, or moderation-sensitive content unless retention and deletion controls are understood.

## Reference(s):

- [BlueColumn API Documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends selected Discord conversation summaries to an external persistent memory service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
