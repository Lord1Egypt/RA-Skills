## Description: <br>
Diagnostic framework to identify and reduce token waste in OpenClaw deployments by applying efficient data handling and model-use practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thebrierfox](https://clawhub.ai/user/thebrierfox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to diagnose token waste, compare inefficient and optimized session patterns, and apply practical cost-control habits for agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cost examples and model-pricing comparisons may become stale or may not match a user's provider contract. <br>
Mitigation: Validate recommendations against current provider pricing and measured token usage before using them for budget decisions. <br>
Risk: Aggressive context reduction or model routing can reduce answer quality if applied without measurement. <br>
Mitigation: Instrument input tokens, output tokens, cost, and task quality, then apply routing and summarization changes incrementally. <br>
Risk: Applying workflow changes directly to production services can affect billing, data exposure, or moderation targets. <br>
Mitigation: Review proposed changes before production use and keep normal secret-handling practices in place. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/thebrierfox/free-token-optimization-primer) <br>
- [Token Cost Intelligence on Claw Mart](https://www.shopclawmart.com/listings/token-cost-intelligence-openclaw-optimization-framework-a417717e) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with diagnostic questions, a cost comparison table, and operating practices] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
