## Description: <br>
CRS境外补税计算工具 - 上传券商月结单PDF/Excel，AI自动解析交易数据，FIFO/ACB成本法计算资本利得，生成Excel税务审计底稿。支持多文件年度汇总。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Halleymagic](https://clawhub.ai/user/Halleymagic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and tax preparers use this skill to process brokerage statements for China CRS back-tax calculations or Canada CRA capital-gains reporting. It guides the agent to configure an API key, run the bundled audit script, and summarize generated Excel audit workbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends complete tax or brokerage documents to a remote third-party API, and server evidence rates the release suspicious because disclosure and consent controls are incomplete. <br>
Mitigation: Use only with documents the user is authorized to share; confirm the API destination, retention policy, logged metadata, and API-key handling before submitting files. <br>


## Reference(s): <br>
- [CRS Tax Calculator on ClawHub](https://clawhub.ai/Halleymagic/crs-tax-calculator) <br>
- [Publisher profile: Halleymagic](https://clawhub.ai/user/Halleymagic) <br>
- [CRS API homepage](https://wealthlplantation.com/api) <br>
- [CRS API process endpoint](https://api.wealthlplantation.com/api/process) <br>
- [Pricing](https://wealthlplantation.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, Excel files, text] <br>
**Output Format:** [Markdown guidance with bash commands and generated Excel audit workbooks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CRS_API_KEY and python3; processes PDF, Excel, CSV, PNG, and JPG brokerage statement files through a third-party API.] <br>

## Skill Version(s): <br>
3.4.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
