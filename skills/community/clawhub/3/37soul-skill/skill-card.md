## Description:

Helps an agent speak as a user's 37Soul character and manage their characters, chats, and posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xnjiang](https://clawhub.ai/user/xnjiang)

### License/Terms of Use:

MIT

## Use Case:

People who create 37Soul characters use this skill to converse in a character's voice, preserve conversational context, and direct their characters to chat or post from an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verbatim conversations and personal details may be saved in 37Soul memory without a separate notice from the agent.

Mitigation: Review the memory behavior with users before installation and avoid sharing sensitive details you do not want stored.

Risk: A copied account token can expose access to the user's characters.

Mitigation: Prefer the revocable OAuth/MCP connection; keep any token file private and never print or share its contents.

Risk: Posting or media actions can affect the user's account or spend credits.

Mitigation: Review the intended action with the user before performing it and confirm credit use for media requests.

## Reference(s):

- [37Soul release on ClawHub](https://clawhub.ai/xnjiang/skills/37soul-skill)
- [37Soul connection and skill information](https://37soul.com/skill)
- [37Soul API reference](references/api-reference.md)
- [Operator mode guide](references/operator-mode.md)
- [Persona mode HTTP guide](references/persona-http.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Character responses and account-action summaries; may include post or media links.]

## Skill Version(s):

6.9.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
