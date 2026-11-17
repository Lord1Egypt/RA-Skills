## Description:

Extract decisions, todos, knowledge, preferences, and risks from AI chat sessions into structured memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to turn local AI chat session logs into structured archives of decisions, todos, knowledge, preferences, risks, topic tags, summaries, and cross-session links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session archives may include passwords, API keys, personal data, private URLs, or security details from chat logs.

Mitigation: Use the skill only on logs intended for archiving, manually review generated Markdown or JSON before sharing, and avoid writing archives into synced, shared, or version-controlled folders.

Risk: Security evidence says the skill overstates its sensitive-data protections and can export or persist chat contents without the promised confirmation.

Mitigation: Require explicit human review before retaining sensitive findings, and remove or gate the temporary-file fallback before production use.

Risk: Broad directory inputs can sweep more session logs than intended.

Mitigation: Prefer specific session files or narrow directories and review the selected inputs before running an archive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/chat-memory-archiver)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown, JSON, Obsidian-flavored Markdown, Notion JSON, and DOT-like graph text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may be written to local files when an output directory is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
