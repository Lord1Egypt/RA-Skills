## Description: <br>
Session retrospective and skill audit. Use when asked to reflect, do a retrospective, review lessons learned, audit what went well or wrong, or review session effectiveness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iliaal](https://clawhub.ai/user/iliaal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to review a completed session, identify mistakes, friction, useful lessons, and skill improvements, and decide which lessons should be persisted for future chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save selected retrospective lessons to memory, which could accidentally capture secrets, customer data, private URLs, or sensitive personal information. <br>
Mitigation: Review the exact content before approving any memory write, and exclude secrets, credentials, customer data, private URLs, and sensitive personal information. <br>
Risk: Retrospective findings or skill audit proposals could introduce incorrect or misleading guidance if accepted without review. <br>
Mitigation: Review proposed findings, memory entries, and skill changes before applying them, then scan the skill before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with review findings, prioritized improvements, proposed diffs, and memory-capture prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose memory entries or skill changes for user approval.] <br>

## Skill Version(s): <br>
3.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
