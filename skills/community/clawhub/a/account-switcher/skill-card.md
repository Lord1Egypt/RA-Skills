## Description: <br>
通过 HTTP API 控制「多账号矩阵管理工具」，实现浏览器账号的启动、关闭和信息查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to list, start, and stop local browser accounts managed by the separate multi-account matrix tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start or stop local browser account sessions through a separate local tool. <br>
Mitigation: Review requested start and stop commands before execution, especially when active account sessions may be interrupted. <br>
Risk: The helper depends on a local HTTP API for the separate multi-account matrix tool. <br>
Mitigation: Use it only with a trusted local installation and keep the API bound to localhost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wociaozhongyunonghaole/account-switcher) <br>
- [Multi-account matrix tool](https://zmt.scys6688.com/) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text results and Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes UTF-8 command results to last_result.txt after local API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
