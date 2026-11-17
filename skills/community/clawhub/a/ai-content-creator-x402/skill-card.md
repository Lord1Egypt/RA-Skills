## Description:

AI content creation via Spraay x402 for blog posts, social media, newsletters, scripts, product copy, image generation, video, text-to-speech, speech-to-text, and web research, with prompts sent to external paid LLM and media APIs using USDC micropayments on Base or Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research topics, draft marketing and editorial copy, generate or transform media, and assemble content workflows through paid Spraay x402 API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, URLs, drafts, audio, and other media may be sent to external paid providers through the Spraay gateway.

Mitigation: Use non-sensitive inputs and avoid proprietary, customer, legal, or confidential content unless external provider processing and retention are acceptable.

Risk: Multi-step content workflows can trigger several paid calls and debit USDC from the agent wallet.

Mitigation: Use a dedicated wallet with limited funds and confirm expected costs before chained workflows, especially video generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plagtech/skills/ai-content-creator-x402)
- [Publisher profile](https://clawhub.ai/user/plagtech)
- [Spraay x402 gateway](https://gateway.spraay.app)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Generated media references]

**Output Format:** [Markdown guidance with bash command examples and JSON API payloads; endpoint responses may include generated content or media URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and curl; calls are sent to external paid APIs through Spraay x402 and may debit USDC per request.]

## Skill Version(s):

1.0.1 (source: server release metadata and target metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
