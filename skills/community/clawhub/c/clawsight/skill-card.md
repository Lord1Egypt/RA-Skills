## Description: <br>
An embedded UX research skill that continuously studies how users interact with OpenClaw by observing conversation patterns, task completions, friction points, satisfaction levels, and micro-survey responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giulianomorse](https://clawhub.ai/user/giulianomorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and product teams use this skill to collect local UX research observations, task-level micro-survey feedback, and daily Markdown insight reports about agent usage patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill records near-verbatim conversation data across sessions by default, which can expose private or confidential context in local logs. <br>
Mitigation: Install only for intentional UX research sessions, avoid use during sensitive work, and review or delete ~/.uxr-observer data regularly. <br>
Risk: Generated reports may contain verbatim user feedback or summaries that should not be shared broadly without review. <br>
Mitigation: Inspect Markdown reports before emailing, downloading, or setting recurring delivery, and share only in response to explicit user intent. <br>
Risk: Always-on observation can continue beyond the user's intended study window. <br>
Mitigation: Use the documented pause, stop, and delete controls when observation is no longer wanted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/giulianomorse/clawsight) <br>
- [Publisher profile](https://clawhub.ai/user/giulianomorse) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSONL observation and survey records, local JSON configuration, and Markdown daily reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores data locally under ~/.uxr-observer/ and only shares reports when the user explicitly requests sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
