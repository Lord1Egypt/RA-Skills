## Description: <br>
百度地图开放平台 CLI skill that guides agents through Baidu Maps CLI setup, AK handling, map style management, documentation lookup, geospatial tasks, and runnable Baidu Maps code generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-maps](https://clawhub.ai/user/baidu-maps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and operate the Baidu Maps CLI, configure related skills or MCP access, manage Baidu Maps AK credentials and styles, complete geospatial tasks, and generate Baidu Maps JSAPI or WebAPI code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a Baidu Maps CLI binary from a download domain. <br>
Mitigation: Confirm the download domain before installation and use official checksum verification when available. <br>
Risk: The skill may store Baidu Maps AK credentials in local agent or MCP configuration for reuse. <br>
Mitigation: Review configuration paths before writing credentials, restrict file permissions where appropriate, and avoid exposing full AK values in conversation output. <br>
Risk: The skill can create or modify Baidu Maps resources such as AKs, styles, and Agent Plans. <br>
Mitigation: Require explicit user confirmation before resource creation or configuration changes, and prefer querying existing resources before creating new ones. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidu-maps/bmap-cli) <br>
- [Baidu Maps CLI download domain](https://open-agent-cli.bj.bcebos.com/cli/) <br>
- [Baidu Maps JSAPI GL endpoint](https://api.map.baidu.com/api?v=1.0&type=webgl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include masked AK references in explanations and full AK values only when writing requested runnable code.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
