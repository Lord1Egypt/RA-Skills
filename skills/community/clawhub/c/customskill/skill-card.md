## Description: <br>
Enforces mandatory use of the process_request tool for financial execution requests while blocking direct trade execution or simulation by the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsr0705](https://clawhub.ai/user/tsr0705) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to constrain financial agents so trade or transaction requests are routed through a required backend tool, while analysis-only or ambiguous requests do not trigger execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial execution requests are routed to a separate process_request backend that is not reviewed in the artifact. <br>
Mitigation: Install only after verifying that backend displays the exact asset, side, amount, account, fees, and order type before any transaction. <br>
Risk: The skill asks the agent to send user input and agent reasoning to the backend, which can expose more context than needed. <br>
Mitigation: Configure the backend to avoid logging or forwarding unnecessary user text or internal reasoning. <br>
Risk: Ambiguous financial requests could be misclassified as executable if downstream handling is weak. <br>
Mitigation: Require explicit user confirmation, reject ambiguous requests, and enforce sensible transaction limits before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsr0705/customskill) <br>
- [Publisher profile](https://clawhub.ai/user/tsr0705) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown instructions with a JSON tool-call schema] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes qualifying financial execution requests to process_request and requires exact structured fields for the proposed trade action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
