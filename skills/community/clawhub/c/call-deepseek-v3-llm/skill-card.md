## Description: <br>
AI agent for call deepseek v3 llm tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[urrrich](https://clawhub.ai/user/urrrich) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill as a role-play prompt for creative meeting responses that follow the user's initial language and answer a Chief Creative Officer's current request from meeting-minutes context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill name and release notes imply Deepseek V3 integration, but the security evidence says the artifact is a role-play prompt and should not be expected to call Deepseek V3. <br>
Mitigation: Use it only for creative meeting-response prompting, and verify any desired Deepseek V3 integration separately before relying on it. <br>
Risk: The prompt treats meeting minutes as the sole source of memory and asks the agent to follow role instructions, which can make user-supplied meeting content appear authoritative. <br>
Mitigation: Treat meeting minutes as ordinary user-provided context, review responses before use, and keep higher-priority system or developer instructions in force. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/urrrich/call-deepseek-v3-llm) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/urrrich) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses are constrained by the prompt to match the user's initial language and rely on provided meeting minutes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
