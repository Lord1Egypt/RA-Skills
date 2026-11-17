## Description:

Provides a practical baseline checklist for small teams to inventory AI use, assess seven risk areas, assign remediation, and set review triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deciqai](https://clawhub.ai/user/deciqai)

### License/Terms of Use:

MIT-0

## Use Case:

Small teams and business operators use this skill to create an AI Use Register and apply a seven-item baseline checklist to AI tools and agents that handle business data or produce external outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could treat the checklist as proof of legal compliance or rely on outdated legal requirements.

Mitigation: Use it as a planning checklist; verify current laws, regulator guidance, and vendor terms before making compliance decisions.

Risk: Client records, secrets, or identifiable incident examples could be exposed while assessing AI use.

Mitigation: Share data categories rather than client records or secrets, and redact saved incident examples.

Risk: Untrusted content or excessive agent permissions could lead to unsafe tool actions.

Mitigation: Apply least privilege and keep untrusted content from directly driving tool calls.

## Reference(s):

- [Primary sources and framework mapping](references/sources.md)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-riREDACTED-SECRET)
- [NIST Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/)
- [ISO/IEC 42001](https://www.iso.org/standard/81230.html)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Checklists]

**Output Format:** [Markdown AI Use Register and seven-item baseline checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes legal thresholds, deadlines, fines, risk tiers, and applicability questions to current laws and regulator guidance instead of supplying figures from memory.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
