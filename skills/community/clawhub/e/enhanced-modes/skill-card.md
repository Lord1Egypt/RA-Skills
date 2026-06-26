## Description: <br>
Provides Explore, Plan, and Verify agent modes plus feature flags for dynamically controlling agent behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayiv-ai](https://clawhub.ai/user/mayiv-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to switch an agent between read-only exploration, plan-first work, and post-action verification, and to toggle advanced behavior flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional memory persistence can scan, update, or archive notes without enough scope clarity. <br>
Mitigation: Keep auto_memory disabled unless it is explicitly needed, and require confirmation before any memory scan, long-term memory update, or note archive. <br>
Risk: Optional background tasks and sub-agent runs can operate with limited user oversight. <br>
Mitigation: Keep autonomous_crons disabled unless it is explicitly needed, and require confirmation before any scheduled task or spawned sub-agent run. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/mayiv-ai/enhanced-modes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with slash-command examples and JSON feature-state configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Feature flags control optional memory consolidation, coordination, verification, and background task behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
