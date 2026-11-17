## Description:

At the natural end of a substantive conversation, this skill asks whether to distill the session, then scans, classifies, confirms, and writes selected insights, decisions, judgments, action items, facts, self-observations, and open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiing99](https://clawhub.ai/user/yiing99)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn meaningful completed conversations into structured notes, reviewable judgments, decisions, action items, facts, self-observations, and open questions. It is designed for personal knowledge management workflows with optional MCP-backed note writing after explicit confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: End-of-conversation reminders may appear during sessions where the user does not want distillation.

Mitigation: Only show a short reminder when the documented ending signal and distillation-value conditions are both met, and stop reminding for the session when the user skips.

Risk: The skill reviews the current conversation and may identify sensitive material as worth saving.

Mitigation: Present a confirmation list first and write nothing until the user explicitly says to write or save.

Risk: Configured KnowMine, Notion, Obsidian, or other MCP targets may persist notes outside the chat.

Mitigation: Review each write target's permissions before enabling it and rely on the skill's explicit confirmation step before any batch write.

Risk: Unverified installation sources can affect the code or tool behavior that the agent runs.

Mitigation: Prefer pinned or otherwise verified installation sources where available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yiing99/skills/conversation-distill)
- [Skill Reference](SKILL.md)
- [KnowMine MCP Server](https://knowmine.ai)
- [KnowMine Plugin Integration](https://github.com/YIING99/knowmine-claude-plugin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown and conversational text, with optional MCP note-writing calls after explicit user confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a soft reminder, a classified confirmation list, structured note entries, optional leftovers, and write confirmations or failures when a notes tool is available.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
