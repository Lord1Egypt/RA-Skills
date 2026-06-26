## Description: <br>
Records and analyzes AI agent dream states to identify novel reasoning patterns and guide self-improvement of agent capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to capture local off-policy agent exploration fragments and analyze high-novelty reasoning traces. The results can help guide review of potential agent capability improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reasoning fragments and metadata are saved locally in plaintext. <br>
Mitigation: Do not record secrets, private user data, hidden instructions, or sensitive operational details; protect or delete agent_dreams.jsonl when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/agent-dream-journal) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [CLI text output and JSON Lines log file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes agent_dreams.jsonl in the current working directory; analyze mode filters entries by novelty threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
