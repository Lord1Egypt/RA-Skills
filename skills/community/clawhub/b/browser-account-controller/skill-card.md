## Description: <br>
通过 HTTP API 控制本地多账号矩阵管理工具，用于启动、关闭和查询浏览器账号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wociaozhongyunonghaole](https://clawhub.ai/user/wociaozhongyunonghaole) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent list, start, and stop accounts in a local multi-account browser management tool by account name or index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start, stop, and list accounts in a separate local browser-account management tool. <br>
Mitigation: Install only when agent control of those accounts is intended, and verify account names or indexes before executing start or stop commands. <br>
Risk: Account names and command results may be written to last_result.txt in the skill directory. <br>
Mitigation: Keep the skill directory access-controlled and remove last_result.txt when command history is no longer needed. <br>
Risk: Changing the API URL away from localhost could expose account-control commands to an unintended service. <br>
Mitigation: Keep api_url pointed at http://localhost:1008 unless a trusted local deployment requires a different endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wociaozhongyunonghaole/browser-account-controller) <br>
- [多账号矩阵管理工具](https://zmt.scys6688.com/) <br>
- [Python downloads](https://www.python.org/downloads/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command results are written to last_result.txt in UTF-8 and should be read from that file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
