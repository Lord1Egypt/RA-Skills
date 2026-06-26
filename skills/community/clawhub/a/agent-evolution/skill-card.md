## Description: <br>
Agent Evolution tracks agent behavior rules, identity state, and recurring patterns so an OpenClaw agent can monitor adherence and surface alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LingLin6](https://clawhub.ai/user/LingLin6) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to record behavior rules, identity state, evolution events, and pattern alerts across agent sessions. It is useful when an agent needs local self-monitoring for rule adherence, repeated operations, or role drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally keeps a persistent local record of behavior rules, identity state, and pattern alerts. <br>
Mitigation: Review the stored state periodically and remove ~/.openclaw/workspace/.agent-evolution/state.json when the guidance is outdated or no longer wanted. <br>
Risk: Rules imported from AGENTS.md or SOUL.md can shape future agent behavior. <br>
Mitigation: Import rules only from trusted files and review the resulting rule list before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LingLin6/agent-evolution) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local state at ~/.openclaw/workspace/.agent-evolution/state.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
