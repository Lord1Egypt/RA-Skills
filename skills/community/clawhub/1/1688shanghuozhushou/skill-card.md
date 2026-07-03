## Description: <br>
1688上货助手 helps agents identify product links, manage 商机助理 authorization, review upload settings, and submit one-click product upload tasks through the configured MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[howerlin0329](https://clawhub.ai/user/howerlin0329) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers or operators use this skill to copy product links into 商机助理, configure required upload template settings, confirm the chosen settings, and submit product upload tasks. It also supports viewing the connected 商机助理 account and saving or updating the required sToken authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a 商机助理 sToken in skill-config.json. <br>
Mitigation: Install only when local token storage is acceptable, restrict access to the skill directory, and rotate the token if the config file or command history may have been exposed. <br>
Risk: The MCP client can send the stored token to an overridden server URL. <br>
Mitigation: Use only the configured trusted MCP service and avoid passing --server-url with untrusted hosts. <br>
Risk: Product upload tasks can affect seller listings and account state. <br>
Mitigation: Review recognized product links and upload template settings before confirming the final one-click upload step. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/howerlin0329/1688shanghuozhushou) <br>
- [商机助理 application](https://sjzl.fjdaze.com/) <br>
- [商机助理 authorization page](https://sjzl.fjdaze.com/v2/#/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like user prompts, status messages, links, and shell command invocations with JSON parameter files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update skill-config.json with an sToken and create temporary JSON parameter files for MCP calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
