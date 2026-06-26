## Description: <br>
Recover conversation context when a message arrives with unclear meaning by checking recent messages, transcripts, channel summaries, cross-channel history, and memory files before asking the user for clarification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yozu](https://clawhub.ai/user/yozu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to help an agent reconstruct missing conversation context across local transcripts, channel summaries, memory files, and cross-channel history before escalating to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to search local conversation history and memory files that may contain sensitive personal data or secrets. <br>
Mitigation: Install only when local history recall is desired, keep indexed folders and channels limited, and avoid sharing raw transcript search output. <br>
Risk: Search results may surface snippets from prior sessions in logs or public channels if handled carelessly. <br>
Mitigation: Review retrieved context before using it in a response and do not pipe search output to public logs or channels. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yozu/agent-session-recall) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown guidance with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local session and memory file paths; no network output is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
