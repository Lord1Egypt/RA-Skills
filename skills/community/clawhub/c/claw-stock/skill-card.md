## Description:

Claw Stock is a Chinese-language single-stock analysis skill that analyzes A-share, Hong Kong, and US equities with dynamic factor selection, scoring, and educational disclaimers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request Chinese-language educational analysis of individual A-share, Hong Kong, and US stocks. It classifies the stock, selects six relevant analysis factors, scores the result, and supports follow-up questions while preserving an investment-risk disclaimer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill discusses stock ratings and buy/sell considerations that users could mistake for investment advice.

Mitigation: Keep the educational disclaimer in outputs and verify current market data independently before relying on any analysis.

Risk: Broad trigger wording may route ambiguous stock-related prompts to this skill.

Mitigation: Narrow trigger language during publication or review so the skill activates only for clear single-stock analysis requests.

## Reference(s):

- [Claw Stock homepage](https://github.com/your-org/claw-stock)
- [ClawHub skill page](https://clawhub.ai/yoborlon-alpha/skills/claw-stock)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese-language stock analysis with factor scores, summary rating, follow-up answers, and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, credential access, or hidden data movement was identified in security evidence.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
