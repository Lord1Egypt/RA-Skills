## Description: <br>
Converts HAR files, Claude Code JSONL logs, and Copilot CLI JSONL logs into structured ATIF v1.6 trajectory JSON using the atifact CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert recorded agent sessions from HAR or JSONL logs into ATIF trajectory JSON for review, analysis, or downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HAR, JSONL, generated trajectory JSON, and stdout pipelines may contain sensitive session data. <br>
Mitigation: Redact secrets before sharing and store or delete generated outputs according to privacy requirements. <br>
Risk: The workflow depends on the external atifact npm package. <br>
Mitigation: Install and run the CLI only when the package is trusted for the intended environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/waldekmastykarz/atifact) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell commands that produce ATIF trajectory JSON files or JSON on stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include main and subagent trajectory files derived from the selected output prefix.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
