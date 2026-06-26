## Description: <br>
药企院外新媒体 AI 运营平台。当用户需要医药内容创作、合规审核、患者管理、竞品分析、药房运营、医生触达或运营分析时触发。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gptplusplus](https://clawhub.ai/user/gptplusplus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharma operations, medical affairs, compliance, and marketing teams use this skill to plan off-hospital media operations, draft and optimize content, review medical advertising compliance, manage patient follow-up, monitor inventory and procurement, analyze competitors, coordinate doctor or KOL outreach, and summarize operational metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive patient and doctor data and change operational records without clear safeguards. <br>
Mitigation: Install only in a controlled test or internal environment with a dedicated non-production database account, and add authorization, confirmation, audit, and retention controls before real use. <br>
Risk: Initialization and database tools could affect real pharma operations data if run against production systems. <br>
Mitigation: Do not run initialization scripts or bundled database tools against production data; review connection settings and isolate the database before execution. <br>
Risk: Patient, doctor, compliance, procurement, and inventory features represent privileged workflows. <br>
Mitigation: Treat those workflows as privileged operations and require human review before acting on generated recommendations or record changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gptplusplus/digitalsalesclaw) <br>
- [Publisher profile](https://clawhub.ai/user/gptplusplus) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Tool manual](artifact/TOOLS.md) <br>
- [Knowledge index](artifact/knowledge/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text, with Python tool outputs and SQL-backed operational summaries when tools are executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query or modify MySQL-backed pharma operations records through bundled Python tools.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
