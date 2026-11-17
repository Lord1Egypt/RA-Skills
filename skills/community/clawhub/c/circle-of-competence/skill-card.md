## Description:

Circle of Competence helps agents coach users through consequential decisions by testing whether the user has calibrated expertise, then recommending decisive action, deferral, waiting, or a smaller bet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business decision-makers use this skill to assess whether an investment, acquisition, hire, market entry, AI initiative, or other consequential decision sits inside their demonstrated competence. The skill guides the agent to identify the domain boundary, document calibration evidence, and choose act, defer, wait, or small-bet responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat coaching output as authoritative advice for investment, hiring, legal, or business decisions.

Mitigation: Present the output as decision coaching, require qualified human or domain-expert review, and keep accountability with the user for consequential decisions.

Risk: The framework may over-discourage action in unfamiliar but learnable or frontier domains.

Mitigation: Apply the skill's documented exceptions for small reversible learning bets and genuinely frontier domains, and size exploratory bets to uncertainty.

Risk: The circle classification depends on user-provided self-assessment, which can be biased or incomplete.

Mitigation: Ask for measurable past outcomes, calibration data, articulable drivers, and expert credibility before classifying a decision as inside the user's circle.

## Reference(s):

- [Primary Sources](references/sources.md)
- [Buffett 1996 Letter to Shareholders](https://www.berkshirehathaway.com/letters/1996.html)
- [How Snapple Got Its Juice Back](https://hbr.org/2002/01/how-snapple-got-its-juice-back)
- [FTC: Keep Your AI Claims in Check](https://www.ftc.gov/business-guidance/blog/2023/02/keep-your-ai-claims-check)
- [SEC Press Release 2024-36](https://www.sec.gov/newsroom/press-releases/2024-36)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown decision-coaching response or filled circle-evaluation template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May pause for user input during novice coaching; no tool calls or code execution are described.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
