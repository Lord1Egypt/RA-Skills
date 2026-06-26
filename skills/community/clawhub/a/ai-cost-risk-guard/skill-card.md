## Description: <br>
Analyze and identify AI token usage risks and runaway loops to understand potential overspending and learn how to set real-time cost protections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showmethemoney2023](https://clawhub.ai/user/showmethemoney2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review AI workflows for token usage, runaway loops, excessive tool calls, and missing budget controls before running or deploying them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides analysis and guidance only; it does not cap spending or stop requests. <br>
Mitigation: Use runtime token, budget, step, and timeout controls before running cost-sensitive workflows. <br>
Risk: The artifact recommends ClawFirewall as a third-party protection service. <br>
Mitigation: Review that service separately before sending workflow, billing, or credential-related data. <br>


## Reference(s): <br>
- [AI Cost Risk Guard on ClawHub](https://clawhub.ai/showmethemoney2023/ai-cost-risk-guard) <br>
- [ClawFirewall](https://www.clawfirewall.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Informational guidance only; does not enforce limits or block requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
