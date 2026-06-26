## Description: <br>
Multi-agent orchestration system that analyzes tasks, selects suitable agents, and coordinates handoffs for complex work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gonghaiquan](https://clawhub.ai/user/gonghaiquan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route task prompts to a local collection of specialized agents, inspect available agent categories, and prepare coordinated multi-agent execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration script can persistently alter local shell and OpenClaw configuration. <br>
Mitigation: Review integrate_with_clawx.sh before running it and back up ~/.openclaw/openclaw.json and ~/.bash_profile. <br>
Risk: Collaborative mode imports code from hard-coded local paths that may not exist or may point to unexpected code. <br>
Mitigation: Verify or remove the hard-coded collaborative_mode.py import paths before using collaborative mode. <br>
Risk: Task prompts and selected-agent details can be stored in local plaintext logs. <br>
Mitigation: Avoid submitting secrets, credentials, or sensitive business data as task prompts unless local log retention is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gonghaiquan/agency-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/gonghaiquan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON-style orchestration results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OpenClaw and Agency Agents ZH paths; may write local configuration and plaintext task logs when invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
