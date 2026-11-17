## Description:

AI assisted Chinese daily diary skill that reviews the day's conversation history, extracts key events, decisions, and insights, and generates a structured diary draft for user review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyu925065781](https://clawhub.ai/user/luyu925065781)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn daily agent conversation history into a private, structured Chinese diary draft, then review, supplement, and archive it locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes broad daily conversation history and may access persistent profile or memory files to match the user's writing style.

Mitigation: Install only when this private-history review is acceptable, keep diary drafts owner-only, and require review before recurring automatic saving or sending.

Risk: The cron example includes group-message delivery for diary content, which could expose private diary drafts.

Mitigation: Before enabling scheduled delivery, replace group chat delivery with a private owner-only destination and verify the channel and recipient.

Risk: Diary drafts could accidentally include secrets, credentials, or personal sensitive information from conversation history.

Mitigation: Apply the skill's sensitive-data filtering before saving or sending and omit uncertain sensitive content.

## Reference(s):

- [Daily Diary ClawHub skill page](https://clawhub.ai/luyu925065781/skills/daily-diary-zh)
- [Diary template](assets/diary-template.md)
- [Diary prompt question bank](references/quick-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown diary draft with optional local file archive and cron job JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diary entries are intended for local storage under ~/diary/ after user review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
