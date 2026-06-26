## Description: <br>
Agent Monitor tracks subagent work status, detects prolonged stalled states, and can send activation messages to resume work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor long-running agent workflows, detect idle or stalled subagents, and optionally nudge selected agents to continue. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic activation can interrupt normal long-running agent work if an agent is incorrectly classified as stalled. <br>
Mitigation: Test with --dry-run first, tune thresholds for the task type, and prefer targeted monitoring or allowlists for sensitive workflows. <br>
Risk: Monitoring and steering other agents can create operational noise or unintended continuation messages when scheduled continuously. <br>
Mitigation: Enable logging or human review before scheduled automatic activation, and use longer thresholds for complex tasks. <br>


## Reference(s): <br>
- [ClawHub Agent Monitor listing](https://clawhub.ai/openlark/agent-monitor) <br>
- [Agent Monitor skill definition](artifact/SKILL.md) <br>
- [monitor_agents.py script](artifact/scripts/monitor_agents.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the bundled script can also emit JSON monitoring results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports threshold, target agent, dry-run, auto-activate, and JSON output options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
