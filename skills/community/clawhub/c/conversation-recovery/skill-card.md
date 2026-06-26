## Description: <br>
Redirect: conversation-recovery has been merged into context-preserver. Use context-preserver for session snapshots, recovery, task handoff, context export, and long-running work continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this redirect skill to move from conversation-recovery to context-preserver for session snapshots, recovery, handoff, context export, and long-running work continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may continue invoking the deprecated conversation-recovery skill instead of the merged context-preserver workflow. <br>
Mitigation: Follow the redirect guidance and use context-preserver for snapshots, recovery, task handoff, context export, and long-running work continuity. <br>
Risk: Recovery snapshots may include sensitive account, identity, address, payment, wallet, bank, or order-submission details if used in shopping or similar workflows. <br>
Mitigation: Keep those sensitive actions and final submissions outside the agent workflow, consistent with the server-provided security guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/conversation-recovery) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown and plain-text handoff guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides a suggested snapshot structure for preserving task state before restoration.] <br>

## Skill Version(s): <br>
1.0.1 (source: skill.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
