## Description:

Keeps a local personal diary for the user by saving diary entries, photos, voice notes, and later retrieving or reflecting on them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitmapasset](https://clawhub.ai/user/bitmapasset)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an agent and the Dear Agent MCP server to capture personal life moments into a local diary and ask for recalls, summaries, and reflections over past entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive personal conversations, photos, voice notes, moods, and relationship details into a local diary.

Mitigation: Use explicit save commands or confirmation before saving sensitive entries, and make diary writes visible to the user.

Risk: Diary entries are stored as plaintext markdown in DEAR_AGENT_DIR.

Mitigation: Protect the local diary directory with appropriate filesystem permissions, backups, and device security.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diary entries and conversational responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request local diary tool calls for saving and retrieving entries; entries can include sensitive personal content.]

## Skill Version(s):

0.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
