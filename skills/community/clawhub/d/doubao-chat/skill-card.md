## Description: <br>
Provides command-line chat with the Doubao model through a free API endpoint, with internet search support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bseye520](https://clawhub.ai/user/bseye520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can run a Node.js command to send prompts to Doubao through a third-party API proxy for conversational answers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the user's Doubao session ID and prompts to doubao-free-api.vercel.app. <br>
Mitigation: Install only if comfortable sharing that credential and prompt content with the third-party API proxy; avoid sensitive prompts and prefer a disposable or easily revocable session. <br>
Risk: The release security verdict is suspicious because the proxy behavior is not described with enough warning in the skill. <br>
Mitigation: Verify the proxy operator and review the request behavior before relying on the skill. <br>


## Reference(s): <br>
- [Doubao homepage](https://www.doubao.com) <br>
- [Doubao free API chat completions endpoint](https://doubao-free-api.vercel.app/v1/chat/completions) <br>
- [ClawHub release page](https://clawhub.ai/bseye520/doubao-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text responses with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, and DOUBAO_SESSIONID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
