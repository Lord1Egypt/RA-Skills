## Description:

Generate concise, user-friendly flight price summaries with buy/wait recommendations. Requires SerpAPI key for real-time price data. Use when users ask about flight prices, purchase timing, or price trends. Designed for C-end chat interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyikoi](https://clawhub.ai/user/keyikoi)

### License/Terms of Use:

MIT-0

## Use Case:

External end users and chat agents use this skill to turn flight price data into concise Markdown price analysis and buy-or-wait guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a SerpAPI key for real-time flight price data.

Mitigation: Configure SerpAPI only in the intended project and use a limited API key where possible.

Risk: Broad trigger wording may activate the skill on generic price questions.

Mitigation: Narrow trigger patterns or route only flight-related price questions to this skill.

Risk: Flight price recommendations can be misleading when historical data is sparse or unavailable.

Mitigation: Label limited data as reference-only and ask users to gather more flight searches or compare current prices before purchasing.

## Reference(s):

- [Price analysis algorithm](artifact/references/price-analysis.md)
- [Copywriting templates](artifact/references/copywriting-templates.md)
- [SerpAPI sign-up](https://serpapi.com/users/sign_up)
- [ClawHub skill page](https://clawhub.ai/keyikoi/skills/flight-price-advisor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise price summaries, simple comparison tables, trend labels, and buy/wait recommendations; notes when price data is limited.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
