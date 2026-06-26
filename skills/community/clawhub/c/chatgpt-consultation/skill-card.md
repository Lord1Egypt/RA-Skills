## Description: <br>
Consults ChatGPT through a browser session when a question is complex, outside the agent's knowledge, or explicitly requests ChatGPT. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahaoxiong](https://clawhub.ai/user/mahaoxiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to consult ChatGPT for technical, knowledge, creative, or complex questions and return the resulting answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user questions through a logged-in browser session, which may expose sensitive prompts to a third-party service. <br>
Mitigation: Use only with non-sensitive questions, notify the user before consultation, and prefer a dedicated browser profile. <br>
Risk: The included script builds a shell command from user-controlled text. <br>
Mitigation: Do not run the script until command execution is changed to safe argument passing and reviewed before deployment. <br>
Risk: The artifact references helper and configuration files that are not included for review. <br>
Mitigation: Include and review the referenced helper script and configuration before installing or operating the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mahaoxiong/chatgpt-consultation) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text with ChatGPT response text and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include third-party ChatGPT content and error messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
