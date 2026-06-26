## Description: <br>
Core decision engine for Ads Manager Specialist; auto-calls tools for Facebook ads URLs, campaign queries, competitor research, budget, and performance tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Phap1106](https://clawhub.ai/user/Phap1106) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Ads operators and agents use this skill to route Meta ads, campaign reporting, competitor research, budget, proposal, approval, and content-related requests into a strict tool-calling workflow. It is intended for credential-backed ad operations where the agent can call configured ads, search, HTTP, and memory tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad automatic authority over credential-backed ad, search, memory, approval, and generic HTTP workflows. <br>
Mitigation: Install only with least-privilege credentials and confirm which approval or rejection actions can change live systems before use. <br>
Risk: Competitor findings and operational notes may be saved to memory and reused later. <br>
Mitigation: Ensure saved competitor memory can be inspected, corrected, and deleted according to the operator's data-retention expectations. <br>
Risk: The skill intentionally discourages clarification questions and pushes immediate tool execution. <br>
Mitigation: Use it only in environments where automatic tool use is expected, monitored, and constrained by external tool permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Phap1106/ads-claw2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, tool calls] <br>
**Output Format:** [Markdown responses and structured tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primarily Vietnamese user-facing ads reports, competitor analyses, proposals, and proactive observations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
