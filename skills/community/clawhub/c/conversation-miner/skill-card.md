## Description:

Conversation Miner helps agents summarize AI conversations and extract structured todos, ideas, decisions, code snippets, and feedback-oriented follow-up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanwan2qq](https://clawhub.ai/user/wanwan2qq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to mine recent AI chat history for summaries, action items, ideas, decisions, code excerpts, and Markdown exports. It is intended for personal or workflow knowledge capture where the user is comfortable with conversation-history analysis and optional persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads recent conversation history, which may include secrets or confidential information.

Mitigation: Use it only on conversations suitable for summarization, and avoid chats containing secrets or confidential data.

Risk: The skill can persist summaries, feedback, preferences, and exports.

Mitigation: Confirm save and export actions deliberately, review generated content, and remove stored files that should not be retained.

Risk: The bundled CLI has unsafe local file-write paths when untrusted --user, MINER_USER, MINER_DATA_DIR, or --output values are supplied.

Mitigation: Do not run the CLI with untrusted path-related inputs until path validation and export containment are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanwan2qq/skills/conversation-miner)
- [README](artifact/README.md)
- [HELP](artifact/HELP.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown summaries and structured text lists, with optional Markdown exports and fenced code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save conversation summaries, feedback, preferences, and exports when the user confirms or invokes export features.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
