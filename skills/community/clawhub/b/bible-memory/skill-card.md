## Description:

Memorize Bible verses with Remember Me, the Bible memory app with spaced repetition. Use when the user wants to memorize, learn by heart or keep a Bible verse, review or be quizzed on their memory verses, read today's passages from a one-year Bible reading plan, or find a ready-made collection of verses to memorize. Works through the Remember Me MCP tools (add_verse, get_review_queue, get_daily_reading, browse_collections and others).

This skill is ready for commercial/non-commercial use.

## Publisher:

[pschaffl](https://clawhub.ai/user/pschaffl)

### License/Terms of Use:

MIT-0

## Use Case:

External Remember Me users can add and organize Bible verses, review due verses, read daily passages from a one-year plan, and discover published verse collections through an assistant.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect verse wording or account selection could affect the user's memorization materials.

Mitigation: Use the exact requested translation and confirm the correct account and label before making changes.

Risk: Changes to a published collection can affect its subscribers.

Mitigation: Confirm with the user before changing a collection they publish.

Risk: A benign security scan does not guarantee zero risk.

Mitigation: Review the skill description and permissions, and install only if they fit your needs.

## Reference(s):

- [Remember Me MCP documentation](https://www.remem.me/docs/mcp/)
- [Remember Me connection guide](references/connect.md)
- [Remember Me vocabulary](references/vocabulary.md)
- [ClawHub release page](https://clawhub.ai/pschaffl/skills/bible-memory)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Conversational text and Remember Me MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool calls may add, update, or delete verses and collections in the signed-in user's account.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
