## Description: <br>
Cognitive Flexibility Release helps an agent choose among OOA, OODA, OOCA, and OOHA cognitive modes for reasoning, pattern matching, creative exploration, discovery, self-assessment, and usage monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alpha963852](https://clawhub.ai/user/alpha963852) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add automatic cognitive mode selection, multi-step reasoning, metacognitive scoring, and local usage reports to complex agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save raw task and context data in local logs. <br>
Mitigation: Disable monitoring for sensitive work or restrict, rotate, and delete logs before using the skill with confidential customer or business data. <br>
Risk: Requested tools are broader than the code appears to require. <br>
Mitigation: Review permissions before installing and remove unused access such as sessions_send, web_search, or Edit when they are not needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alpha963852/cognitive-flexibility) <br>
- [OODA mode guide](references/ooda-guide.md) <br>
- [Monitoring guide](MONITORING-GUIDE.md) <br>
- [Release notes](RELEASE-NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and Python-oriented guidance with optional JSON usage logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local usage logs and statistics when monitoring is enabled.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
