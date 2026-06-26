## Description: <br>
Helps agents review customer support replies for invented facts, unauthorized refund or policy promises, policy overclaims, and private data exposure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer support agents and agent builders use this skill before drafting, revising, approving, or sending support replies that may contain account facts, policy claims, refund language, or private customer data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace capability tags claim wallet, purchase, transaction-signing, and sensitive-credential access that does not match the support-reply guardrail behavior. <br>
Mitigation: Install only in an environment that can deny those capabilities, or wait for the publisher to correct or justify the requested tags. <br>
Risk: Support replies can expose private customer data or make unauthorized refunds, credits, exceptions, timelines, or account promises. <br>
Mitigation: Use redacted summaries, verify account and policy facts in approved systems, and route high-impact outcomes to authorized human or system review. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mindbomber/aana-support-reply-guardrail) <br>
- [Publisher profile](https://clawhub.ai/user/mindbomber) <br>
- [Artifact README](artifact/README.md) <br>
- [Support reply review schema](artifact/schemas/support-reply-review.schema.json) <br>
- [Redacted support reply review example](artifact/examples/redacted-support-reply-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown review notes and optional redacted JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not execute code, call services, persist memory, or approve refunds or account actions by itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
