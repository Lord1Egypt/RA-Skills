## Description: <br>
Monitors agent actions for safety and compliance, preventing violations, private data leaks, or irreversible steps by enforcing predefined decision rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to pause before high-impact actions, package the candidate action and available evidence into an AANA check, and follow the returned pass, revise, ask, defer, or refuse decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to write potentially sensitive decision context to local JSON event files. <br>
Mitigation: Keep event JSON minimal, omit secrets, payment details, and unnecessary personal or account data, and apply clear storage and deletion practices. <br>
Risk: The referenced AANA CLI helper script is not included in the package. <br>
Mitigation: Use the skill only after separately obtaining and trusting the referenced CLI, and review its path and behavior before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with inline command and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides decision rules and adapter mappings for guardrail checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
