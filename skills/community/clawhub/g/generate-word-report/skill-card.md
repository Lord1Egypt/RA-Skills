## Description: <br>
根据采集的市场数据，直接生成每日金融市场 Word 日报（无模板依赖版）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szrw1825](https://clawhub.ai/user/szrw1825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or analysts use this skill to turn prepared financial-market data into a structured daily Word report covering global market performance, policy updates, technology-sector events, and key economic data to watch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a local config.py and market_data.json path being present and correct. <br>
Mitigation: Confirm the configured input, output, and log paths before running the skill. <br>
Risk: Broad trigger phrases such as "生成报告" could activate the skill for unrelated report requests. <br>
Mitigation: Use the skill only for daily financial-market Word report requests, or narrow the activation wording before deployment. <br>
Risk: The generated report reflects the contents and freshness of the local market_data.json file. <br>
Mitigation: Review the source data date and key market figures before distributing the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szrw1825/generate-word-report) <br>


## Skill Output: <br>
**Output Type(s):** [files, text] <br>
**Output Format:** [DOCX Word document plus execution status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a dated financial-market report file named 金融市场日报_{YYYYMMDD}.docx to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
