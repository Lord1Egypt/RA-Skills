## Description: <br>
Generates OpenClaw Agent weekly usage reports by reading session logs and memory files, then summarizing activity, tool calls, cost, and memory notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[56xiaoli123](https://clawhub.ai/user/56xiaoli123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to generate a weekly activity report from local agent session logs and memory notes. The report helps summarize usage volume, frequent tool calls, estimated cost, and notable memory entries for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and reproduce private OpenClaw session and memory data. <br>
Mitigation: Use it only on workspaces whose session and memory contents you intend to review, and inspect the generated report before saving or sharing it. <br>
Risk: The documented workspace option does not fully scope all reads in the current script. <br>
Mitigation: Review the configured OpenClaw paths before running the script and avoid relying on the workspace option as a complete access boundary. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/56xiaoli123/agent-usage-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text weekly report with structured sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print to stdout or save the report to a file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
