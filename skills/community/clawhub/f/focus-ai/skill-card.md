## Description: <br>
focusAI helps an agent work with a local FocusAI setup to monitor screen activity, assess focus, and answer questions about current or historical work context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HR2AY](https://clawhub.ai/user/HR2AY) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using ClawHub agents can use this skill to start, stop, query, and summarize FocusAI screen-monitoring sessions after local setup and explicit consent. It is intended for personal focus tracking, work-history review, and analysis of locally stored screenshot and CSV records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports screen monitoring and can involve sensitive screenshots. <br>
Mitigation: Start monitoring only after explicit user consent, clearly disclose screenshot behavior, and stop or delete local history when it is no longer needed. <br>
Risk: Screenshots may be sent to a user-configured cloud vision provider for analysis. <br>
Mitigation: Review the selected provider settings before use and avoid monitoring private or regulated content unless the user accepts that data flow. <br>
Risk: Local API keys and configuration files are sensitive. <br>
Mitigation: Keep credentials in user-managed local configuration, do not expose keys in agent-readable conversations, and do not read or transmit credential file contents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HR2AY/focus-ai) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/HR2AY) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional inline shell commands and local service guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local FocusAI start commands or HTTP API interactions only after user consent; may summarize local focus history when data exists.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
