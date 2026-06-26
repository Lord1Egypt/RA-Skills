## Description: <br>
Analyze codebases quickly with AI-powered intelligence and insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Codepal to record code review notes, validation findings, generation prompts, explanations, diffs, fixes, and reports, then search or export the local activity history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered content may include secrets, private source code, vulnerability details, or confidential notes and is saved locally for later search or export. <br>
Mitigation: Avoid entering sensitive material unless local persistence is acceptable, review exported files before sharing, and delete ~/.local/share/codepal when the history is no longer needed. <br>
Risk: The skill description may overstate AI analysis capabilities compared with the bundled local logging script. <br>
Mitigation: Treat Codepal as an activity/history logger and verify any code quality conclusions independently. <br>


## Reference(s): <br>
- [Codepal ClawHub page](https://clawhub.ai/xueyetianya/codepal) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output and local log/export files in text, JSON, or CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists command inputs under ~/.local/share/codepal and can export saved history.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
