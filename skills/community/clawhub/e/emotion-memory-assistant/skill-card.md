## Description:

情感记忆助手自动检测用户对话中的正向、负向或中性情绪，记录历史情绪，并在合适时生成关心消息和周报。

This skill is ready for commercial/non-commercial use.

## Publisher:

[786793119](https://clawhub.ai/user/786793119)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents can use this skill to classify Chinese-language conversation snippets by emotion, store recent emotional history, surface care messages after negative sentiment, and generate weekly emotion summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive emotional classifications and short message excerpts in plaintext on the user's machine.

Mitigation: Use the skill only with explicit opt-in, apply restrictive permissions to ~/.memory/emotions/history.json, and add retention limits plus a deletion path before broad use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/786793119/skills/emotion-memory-assistant)
- [Skill-declared Homepage](https://github.com/786793119/miya-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [JSON-like Python dictionaries with text fields and a markdown-style weekly report string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists emotion history locally at ~/.memory/emotions/history.json]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
