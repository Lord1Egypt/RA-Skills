## Description: <br>
Color Adjustment provides AgentPMT-hosted color conversion, manipulation, and palette generation for hex, RGB, HSL, and named CSS colors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and UI builders can use this skill to convert color formats, derive complements or lightness and saturation variants, generate random colors, and create palettes through AgentPMT-hosted remote tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AgentPMT-hosted remote tool calls and may require account or payment setup. <br>
Mitigation: Use the AgentPMT setup skill for credential handling, confirm the 5-credit action cost before invocation, and keep payment headers out of prompts and logs. <br>
Risk: Security evidence flags wallet and sensitive-credential capability tags even though the scan verdict is clean. <br>
Mitigation: Do not include account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts, logs, or color inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/color-adjustment) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/color-adjustment) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON tool-call arguments and returned color values, with Markdown guidance when explaining workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote actions return color results in hex, RGB, and/or HSL formats; most actions cost 5 credits and require AgentPMT account setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
