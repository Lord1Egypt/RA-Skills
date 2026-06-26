## Description: <br>
Detects potential infinite loops and runaway token usage risks in Claw AI workflows by analyzing retry, recursion, and termination conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ShowMeTheMoney2023](https://clawhub.ai/user/ShowMeTheMoney2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review Claw workflows, task descriptions, or agent prompts for retry, recursion, and missing termination-condition patterns that can cause runaway loops and high token costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow or prompt reviews may include confidential prompts, business workflows, or sensitive operational details. <br>
Mitigation: Avoid pasting sensitive material unless it is appropriate for the agent to process; redact confidential details before analysis. <br>
Risk: The skill provides advisory loop-risk analysis and safeguard recommendations that may miss workflow-specific failure modes. <br>
Mitigation: Review the findings before deployment and combine them with concrete controls such as token limits, retry limits, and behavior monitoring. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown risk analysis with lists and short explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Low, Medium, or High risk level, detected loop triggers, token impact estimate, and recommended safeguards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
