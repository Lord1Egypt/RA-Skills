## Description: <br>
Reorder previous Foodora orders and track ETA or status with ordercli, requiring explicit user approval before any order is placed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Foodora users can ask an agent to preview and reorder prior meals through ordercli, then track active delivery status. The skill is intended to stop before checkout unless the user explicitly confirms placing the order. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Foodora login or Chrome profile session to access account order history. <br>
Mitigation: Install only if the user trusts the ordercli project and is comfortable with the selected Foodora authentication method. <br>
Risk: A reorder command with confirmation can place a real food order. <br>
Mitigation: Review the preview carefully and run the confirmation command only after the user explicitly approves placing that order. <br>
Risk: The broad food-ordering trigger could activate when the user is only exploring options. <br>
Mitigation: Use food-specific wording, stop at preview when intent is unclear, and ask clarifying questions before checkout. <br>


## Reference(s): <br>
- [Food Order skill page](https://clawhub.ai/steipete/food-order) <br>
- [ordercli homepage](https://ordercli.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preview-first ordering flow; explicit confirmation required before commands that place an order.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
