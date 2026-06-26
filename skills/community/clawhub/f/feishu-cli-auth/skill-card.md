## Description: <br>
Feishu Cli Auth helps agents guide Feishu OAuth login, user access token refresh, scope selection, and token-related troubleshooting for feishu-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GISwilson](https://clawhub.ai/user/GISwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to complete Feishu OAuth authorization, manage User Access Tokens, choose required scopes, and troubleshoot authentication or permission errors in feishu-cli workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill recommends broad Feishu OAuth scopes, including write-capable calendar and task permissions. <br>
Mitigation: Grant only the scopes needed for the current command when possible, and review the requested permissions before completing OAuth authorization. <br>
Risk: A refresh token is stored locally at ~/.feishu-cli/token.json and can remain valid after the access token expires. <br>
Mitigation: Protect the token file, avoid sharing it in logs or prompts, and delete or revoke the token when access is no longer needed. <br>
Risk: The workflow depends on a local feishu-cli binary that performs OAuth and token refresh operations. <br>
Mitigation: Verify the feishu-cli binary source before use and review authentication commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GISwilson/feishu-cli-auth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include OAuth URLs, callback handling steps, token status checks, scope recommendations, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
