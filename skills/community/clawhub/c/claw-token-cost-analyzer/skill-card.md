## Description: <br>
Analyzes Claw AI workflows to estimate token usage and costs, identify runaway-loop risks, and suggest optimizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShowMeTheMoney2023](https://clawhub.ai/user/ShowMeTheMoney2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent builders use this skill to review Claw workflows, prompts, or task descriptions before deployment and estimate token cost exposure. It highlights retry loops, recursive calls, large context growth, expensive model usage, and practical optimization steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow text submitted for analysis may contain secrets, customer data, proprietary prompts, or business-sensitive automation details. <br>
Mitigation: Review and redact workflow content before pasting it into the analyzer. <br>
Risk: Cost estimates and loop-risk labels are planning guidance rather than guaranteed billing outcomes. <br>
Mitigation: Validate estimates against actual model pricing, usage telemetry, and budget controls before relying on them for production decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ShowMeTheMoney2023/claw-token-cost-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style structured text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a risk level, estimated token and cost range, detected issues, and optimization suggestions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
