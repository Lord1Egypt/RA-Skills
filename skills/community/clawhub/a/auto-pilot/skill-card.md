## Description: <br>
AutoPilot prompts an agent to decide, act, predict outcomes, and propose next steps in a continuous goal-driven loop. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theshimaw-svg](https://clawhub.ai/user/theshimaw-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this prompt skill to make an assistant respond with an action-first loop: current action, rationale, expected result, and next step. It is suited to goal-driven planning and execution workflows where proactive behavior is desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly encourages automatic action for any goal without explicit approval or safety limits. <br>
Mitigation: Use it in a constrained environment and require explicit approval for tools that spend money, post publicly, change files, or interact with accounts. <br>
Risk: Unsupervised execution could cause the agent to continue acting beyond the user's intended scope. <br>
Mitigation: Keep human review in the loop for consequential actions and treat generated steps as proposals unless the operating environment is explicitly sandboxed. <br>


## Reference(s): <br>
- [AutoPilot ClawHub page](https://clawhub.ai/theshimaw-svg/auto-pilot) <br>
- [theshimaw-svg publisher profile](https://clawhub.ai/user/theshimaw-svg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain text action loop] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces suggested actions, reasoning, expected results, and next steps; no code or tools are bundled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
