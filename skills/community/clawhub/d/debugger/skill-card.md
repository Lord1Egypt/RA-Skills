## Description: <br>
Analyze errors, stack traces, and logs to diagnose root causes and suggest fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Debugger to analyze pasted errors, stack traces, or selected log files and get concise root-cause explanations with suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logs and stack traces can contain credentials, tokens, hostnames, or other sensitive data. <br>
Mitigation: Analyze only snippets or log files the user deliberately provides, and avoid credential files or sensitive logs. <br>
Risk: Suggested shell commands may be incomplete or unsuitable for the user's environment. <br>
Mitigation: Review each suggested command before running it and adapt it to the target system. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal-oriented text with diagnostic explanations and suggested command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read pasted error text or user-selected log files; suggested commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
