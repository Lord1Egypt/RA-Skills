## Description:

AI Fortune Teller helps an agent produce Chinese fortune-telling, Bazi, tarot, daily fortune, K-line style life-fortune visualization, past-life portrait, and future-partner portrait outputs using MiniMax text and image models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackjls](https://clawhub.ai/user/jackjls)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for entertainment-oriented Bazi readings, tarot interpretations, daily fortune summaries, and related image prompts or generated image links. It is intended for reflective or entertainment use, not professional, medical, legal, financial, or life-decision advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send names, birth details, questions, and generated prompts to MiniMax.

Mitigation: Use it only when users accept that data sharing, and avoid entering sensitive personal information beyond what is needed for the entertainment workflow.

Risk: API credentials and local environment values may be read from $HOME/.clawd/.env during standalone script use.

Mitigation: Keep unrelated secrets out of that file and review local environment configuration before running the scripts.

Risk: Changing MINIMAX_API_HOST can redirect requests to an untrusted endpoint.

Mitigation: Leave MINIMAX_API_HOST unset or set it only to a trusted MiniMax endpoint.

Risk: Fortune, tarot, and portrait outputs may be mistaken for reliable advice.

Mitigation: Present outputs as entertainment and require users to rely on qualified professionals for consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackjls/skills/ai-fortune-teller)
- [Publisher profile](https://clawhub.ai/user/jackjls)
- [Bazi prompt](artifact/references/bazi-prompt.md)
- [Daily fortune prompt](artifact/references/daily-fortune-prompt.md)
- [K-line generator](artifact/references/kline-generator.md)
- [Tarot prompt](artifact/references/tarot-prompt.md)
- [Usage examples](artifact/references/usage-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, image URLs, JSON, shell commands, guidance]

**Output Format:** [Markdown-style fortune reports, shell output, generated image URLs, and JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image URLs are described by the artifact as valid for 24 hours; standalone scripts require MINIMAX_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
