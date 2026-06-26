## Description: <br>
Provides recent Double Color Ball lottery results, trend analysis, and entertainment-only next-draw number suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltap266](https://clawhub.ai/user/ltap266) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent for recent Double Color Ball draw results, basic trend summaries, and clearly labeled entertainment-only prediction suggestions. The skill is best treated as a convenience lookup and formatting tool, not as a reliable financial or gambling decision aid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The environment check script can inspect local configuration files that may contain credentials or private workspace data. <br>
Mitigation: Review or remove check_env.py before installation, and do not run the skill in workspaces containing secrets in .env, MEMORY.md, TOOLS.md, or OpenClaw configuration files. <br>
Risk: Lottery results may be stale, simulated, or otherwise unverified when network retrieval fails. <br>
Mitigation: Treat all results and predictions as entertainment-only output and independently verify draw data before relying on it. <br>
Risk: Disabled TLS certificate verification can allow lottery data to be tampered with in transit. <br>
Mitigation: Restore certificate verification or run the network retrieval only in a controlled environment after reviewing the code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ltap266/double-color-ball) <br>
- [Publisher Profile](https://clawhub.ai/user/ltap266) <br>
- [China Welfare Lottery Draw Notice API](https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=10) <br>
- [17500 Double Color Ball Information](https://www.17500.cn/ssq/newinfo.php) <br>
- [Baidu Search](https://www.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with lottery result tables, trend summaries, prediction suggestions, and status notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include diagnostic status on data source, freshness, and fallback behavior.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
