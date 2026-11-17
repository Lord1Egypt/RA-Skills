## Description:

Catch stray thoughts, half-sentences, overheard snippets, people, places, links, and gut feelings throughout the day; file them into a same-day archive that preserves the user's original voice; and later surface latent connections across semantic, temporal, emotional, people, and scene threads without drawing conclusions for the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheyuy](https://clawhub.ai/user/sheyuy)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to capture loose thoughts throughout the day, organize same-day fragments by type, and review cross-period connections while preserving the user's original words.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal fragments may include sensitive information that the agent can retain or quote later.

Mitigation: Avoid recording secrets, credentials, or highly sensitive personal details; review connected note-tool permissions before allowing sync.

Risk: Cross-period review may mislead users if connections are interpreted as conclusions.

Mitigation: Use factual connection outputs with original quotes and leave conclusions to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sheyuy/skills/fragment-thoughts-organizer-en)
- [Server-resolved GitHub repository](https://github.com/Sheyuy/fragment-thoughts-organizer-en)
- [Daily Fragment Organizing Method](references/how-to-organize.md)
- [Cross-Period Latent Connections](references/patterns.md)
- [Anti-Patterns: Default Mistakes LLMs Make](references/anti-patterns.md)
- [Example 01: Catching a Single Fragment](references/examples/01-single-fragment.md)
- [Example 02: Daily Archive](references/examples/02-daily-archive.md)
- [Example 03: Cross-Period Connections](references/examples/03-cross-period.md)
- [Example 04: Cross-Period Connections (Conference Day Recap)](references/examples/04-summit-recap.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown responses with preserved user quotes, timestamped fragment entries, daily archives, and cross-period connection lists.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves original wording and avoids conclusions, summaries, pep talks, and proactive browsing.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
