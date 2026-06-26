## Description: <br>
EctoClaw helps OpenClaw agents record signed, hash-chained audit activity, verify session integrity, manage policies, and export compliance reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EctoSpace](https://clawhub.ai/user/EctoSpace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security teams use EctoClaw to log OpenClaw agent activity, verify tamper evidence, review policies, and generate compliance or forensic reports for sessions they operate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit sessions can contain sensitive prompts, tool outputs, memory contents, and agent activity records. <br>
Mitigation: Keep ECTOCLAW_URL on localhost or infrastructure you control, protect exposed servers with authentication, and treat audit logs as sensitive retained records. <br>
Risk: Policy changes can affect whether agent actions are blocked, redacted, flagged, or require approval. <br>
Mitigation: Review policy changes before saving them and confirm the configured rules match the intended controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/EctoSpace/ectoclaw) <br>
- [EctoClaw npm package](https://www.npmjs.com/package/ectoclaw) <br>
- [EctoClaw website](https://ectospace.com/EctoClaw) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries with HTTP API request guidance, JSON payloads, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ECTOCLAW_URL to target a user-controlled EctoClaw server.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
