## Description:

Generate professional customer service scripts for more than 10 industries using AI-assisted reply generation, sentiment analysis, and quality scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Customer service teams, support automation builders, and agent developers use this skill to draft customer replies for complaints, after-sales support, sales conversion, and common service scenarios across industries such as e-commerce, finance, education, and healthcare.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer messages may be sent to the OpenClaw LLM provider, including confidential or regulated customer data.

Mitigation: Use the skill only where external LLM processing is approved, minimize personal data in prompts, and require human review before sending generated replies in sensitive industries.

Risk: The artifact depends on external packages and runtime API credentials.

Mitigation: Install dependencies in an isolated environment with pinned versions, and provide OPENCLAW_API_KEY through managed secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-customer-service-scripts)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Plain text customer-service replies with Python and command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated replies are scored from 0 to 100 by a simple quality heuristic.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
