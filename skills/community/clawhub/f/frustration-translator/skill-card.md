## Description: <br>
Detects user frustration in prompts and translates charged or vague language into clear, actionable instructions for an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dodge1218](https://clawhub.ai/user/dodge1218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help agents recognize emotionally charged task requests, restate the likely actionable need, and proceed with focused execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage agents to persist raw frustrated user messages, which may retain sensitive user content. <br>
Mitigation: Remove or disable the raw quote log unless users have approved that persistence and the log is reviewed under the deployment's data handling rules. <br>
Risk: The skill can encourage agents to act on inferred intent too aggressively. <br>
Mitigation: Keep normal clarification, confirmation, and safety checks for sensitive, costly, public, or irreversible actions even when frustration is detected. <br>


## Reference(s): <br>
- [Frustration Log](references/frustration-log.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance and concise natural-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API, shell, or configuration output is produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
