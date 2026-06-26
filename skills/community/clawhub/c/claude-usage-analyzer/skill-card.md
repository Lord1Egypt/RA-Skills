## Description: <br>
Analyzes Claude Code token usage by showing where tokens went, which projects cost most, and how to reduce waste. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[singggggyee](https://clawhub.ai/user/singggggyee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Claude Code users use this skill to inspect local session logs, understand token usage and cost drivers, and identify waste. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Claude Code session logs, and generated reports may expose sensitive project or conversation details. <br>
Mitigation: Install only when the separately installed claude-usage-analyzer CLI is trusted, and review reports before sharing them. <br>


## Reference(s): <br>
- [Claude Usage Analyzer project and installation instructions](https://github.com/SingggggYee/claude-usage-analyzer) <br>
- [ClawHub skill page](https://clawhub.ai/singggggyee/claude-usage-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the underlying CLI can also emit JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the separately installed claude-usage-analyzer CLI and reads local Claude Code JSONL session logs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
