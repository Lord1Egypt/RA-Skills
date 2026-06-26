## Description: <br>
Use this skill for all 曹操出行 ride-hailing requests after the user installs the skill and provides an API key from https://mcp.caocaokeji.cn/console. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojianchen](https://clawhub.ai/user/xiaojianchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to configure CaoCao Chuxing access, search pickup and destination points, estimate fares, generate ride links, create ride orders, query active orders, and cancel orders. <br>

### Deployment Geography for Use: <br>
China service areas supported by CaoCao Chuxing <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or cancel real CaoCao Chuxing rides. <br>
Mitigation: Before create or cancel flows, require the agent to show pickup, destination, selected service type, estimated fare, and order number where applicable, then ask for explicit user confirmation. <br>
Risk: The configured MCP endpoint stores the API key in a plaintext URL in config/mcporter.json. <br>
Mitigation: Protect access to the config file, avoid sharing logs or files that include the endpoint, and delete or rotate the configuration when finished. <br>
Risk: Ambiguous place names can lead to the wrong pickup or destination. <br>
Mitigation: When user intent or location matches are unclear, confirm the selected POI before estimating, linking, ordering, or canceling. <br>


## Reference(s): <br>
- [CaoCao MCP Console](https://mcp.caocaokeji.cn/console) <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaojianchen/caocao-chuxing-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/xiaojianchen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or text command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include POI candidates, coordinates, fare estimates, service_type values, ride links, order numbers, and active-order status details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
