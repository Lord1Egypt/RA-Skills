## Description: <br>
定时获取档案行业最新情报、政策法规、技术动态和行业资讯。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijie012](https://clawhub.ai/user/lijie012) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Archive professionals, researchers, and operations teams use this skill to gather archive-sector policy updates, industry news, technology trends, and academic developments. It also helps prepare recurring daily, weekly, or monthly intelligence reports from configured sources and keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring scheduled execution may run local collection jobs more often than intended. <br>
Mitigation: Create scheduled tasks only when recurring reports are needed, and review the schedule before enabling automation. <br>
Risk: The helper script writes report files to the configured output directory. <br>
Mitigation: Review the configured output path and file permissions before running the script. <br>
Risk: The security review notes that the provided helper script may need fixing before it works reliably. <br>
Mitigation: Test the script in a controlled environment and correct runtime issues before relying on generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijie012/archive-intelligence) <br>
- [National Archives Administration of China](https://www.saac.gov.cn) <br>
- [State Council policy database](https://www.gov.cn/zhengce/zhengceku/) <br>
- [CNKI](https://www.cnki.net) <br>
- [Wanfang Data](https://www.wanfangdata.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown reports with JSON configuration examples and scheduling commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports include collection time, selected sources, keywords, categorized findings, and source links when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
