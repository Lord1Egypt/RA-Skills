## Description: <br>
Audits OpenClaw exec command transcripts, flags high- and medium-risk command patterns, applies a configurable whitelist, and prints a risk-level report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaodaabao](https://clawhub.ai/user/gaodaabao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review recent OpenClaw shell command history for destructive operations, privilege changes, downloads, package installs, and other commands that may require investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit reads local OpenClaw command transcripts, which may contain secrets, private paths, or operational details. <br>
Mitigation: Use an explicit transcript path when possible and review generated reports for sensitive content before sharing them. <br>
Risk: Whitelist rules can cause risky commands to be reported as OK. <br>
Mitigation: Review and tighten whitelist entries before relying on the audit result, especially broad regex patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaodaabao/audit-exec) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and a plaintext audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local transcript JSONL and applies regex risk rules plus whitelist entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
