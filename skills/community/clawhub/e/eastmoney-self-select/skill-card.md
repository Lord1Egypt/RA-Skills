## Description: <br>
妙想自选管理skill，基于东方财富通行证账户数据及行情底层数据构建，支持通过自然语言查询、添加、删除自选股。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[QQK000](https://clawhub.ai/user/QQK000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query, add, or delete Eastmoney account watchlist entries through natural-language or command-line requests. It is intended for workflows that need watchlist data returned as terminal text and saved CSV or JSON files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add or delete account watchlist entries. <br>
Mitigation: Use explicit query, add, or delete commands and review delete requests before running them. <br>
Risk: The runtime needs access to an Eastmoney API key. <br>
Mitigation: Install only in trusted environments and provide the API key through environment configuration. <br>
Risk: Watchlist query results are saved locally as CSV and JSON files. <br>
Mitigation: Remove saved output files when the watchlist data should not persist on disk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/QQK000/eastmoney-self-select) <br>
- [Eastmoney self-select query API](https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/get) <br>
- [Eastmoney self-select management API](https://mkapi2.dfcfs.com/finskillshub/api/claw/self-select/manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [Terminal text plus CSV and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Query results are saved under the configured output directory using the mx_self_select_ filename prefix.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
