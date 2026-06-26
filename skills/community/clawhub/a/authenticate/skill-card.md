## Description: <br>
Guides agents through signing in to the Finance District agent wallet with the fdx CLI and resolving authentication failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and wallet users use this skill to authenticate a Finance District agent wallet before wallet operations such as sending tokens, swapping, and checking balances. It helps the agent choose the browser or device OAuth flow, check authentication status, and log out when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be triggered by broad login, setup, or connection requests even though it handles sensitive wallet authentication. <br>
Mitigation: Use it only for expected Finance District wallet authentication or explicit fdx authentication failures, and confirm the account and intended wallet action before continuing. <br>
Risk: OAuth prompts and locally stored wallet credentials are sensitive. <br>
Mitigation: Keep the human in control of browser or device authorization, avoid exposing tokens or codes in chat, and use fdx logout on shared or untrusted machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rachidjarray-hk-qa-fdt/authenticate) <br>
- [Finance District MCP server](https://mcp.fd.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts the human to complete browser or device authorization; does not itself produce tokens for display.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
