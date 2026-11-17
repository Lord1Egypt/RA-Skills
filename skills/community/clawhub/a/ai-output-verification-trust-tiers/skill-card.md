## Description:

Helps teams assign verification tiers to AI outputs based on error cost and verifiability, with evidence, escalation, and review rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Teams designing or operating AI workflows use this skill to decide which outputs can be released after lightweight checks, which need human review, and which must remain human-executed. It helps define evidence requirements, escalation triggers, and spot-checking for each output type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readers could treat the tier system as a compliance standard or apply it without assigning human reviewers to consequential outputs.

Mitigation: Use it as a planning framework rather than a compliance standard, and keep named human reviewers responsible for consequential outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deciqai/skills/ai-output-verification-trust-tiers)
- [Sources and references](artifact/references/sources.md)
- [NIST AI 600-1: Generative Artificial Intelligence Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [NIST AI 100-1: AI Risk Management Framework 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf)
- [EU AI Act, Article 14: Human Oversight](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- [Parasuraman and Manzey (2010), automation complacency and bias](https://doi.org/10.1177/0018720810376055)
- [Mata v. Avianca, Opinion and Order on Sanctions](https://law.justia.com/cases/federal/district-courts/new-york/nysdce/1:2022cv01461/575368/54/)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown tables]

**Output Format:** [Text and Markdown, including a trust tier table and verification checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coach one step at a time; specifies source evidence and named human review for consequential outputs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
