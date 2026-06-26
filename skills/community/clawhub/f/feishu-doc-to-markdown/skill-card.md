## Description: <br>
智能转换飞书文档为高可用Markdown格式，自动处理私有资源、无效占位符、冗余引用，生成多版本满足不同场景需求。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whisperbot](https://clawhub.ai/user/whisperbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and teams use this skill to convert Feishu documents into high-density Markdown for archiving, knowledge-base ingestion, and extracting core document information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private Feishu document contents can be copied into local archives or knowledge-base files. <br>
Mitigation: Use the skill only where local archiving is acceptable, choose a safe output directory, and review generated files before committing or sharing them. <br>
Risk: Knowledge-base sync can persist document summaries and extracted points beyond the immediate conversion task. <br>
Mitigation: Leave knowledge-base sync disabled unless intended, and inspect any generated LEARNINGS.md entries before reuse. <br>
Risk: Feishu access depends on plugin permissions and the authorized account. <br>
Mitigation: Verify Feishu plugin permissions and document-read access before processing confidential documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whisperbot/feishu-doc-to-markdown) <br>
- [Publisher profile](https://clawhub.ai/user/whisperbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports raw, enhanced, and optimized conversion modes; may archive source content and optionally update LEARNINGS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
