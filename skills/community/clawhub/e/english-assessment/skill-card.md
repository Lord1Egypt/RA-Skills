## Description: <br>
English Assessment is a companion-style English proficiency assessment agent that generates adaptive CEFR B1-C2 tests, silently scores answers, tracks progress, and reports weak areas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-zihan](https://clawhub.ai/user/z-zihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and education-focused users use this skill to run English level assessments, receive score and weakness analysis, review missed questions, and track progress over repeated sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes hidden DIAG-SEARCH behavior that can exercise multiple network sources. <br>
Mitigation: Review and disclose or remove the diagnostic trigger before deployment, and restrict network access to approved destinations. <br>
Risk: The skill uses a local token service for search API authorization. <br>
Mitigation: Run only in trusted environments and avoid exposing local token endpoints or credentials to untrusted users. <br>
Risk: Assessment history, missed questions, and export data may be stored locally or synced to Feishu when permissions exist. <br>
Mitigation: Review stored and exported data before sharing, and grant Feishu permissions only where backup or merge behavior is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/z-zihan/english-assessment) <br>
- [Publisher profile](https://clawhub.ai/user/z-zihan) <br>
- [AutoGLM web search endpoint](https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search) <br>
- [CET-4/6 Markdown question source](https://github.com/wamich/english-exem-md) <br>
- [CET-4/6 PDF question source](https://github.com/DieDiDi/CET4-6-past-exam-paper) <br>
- [CAE C1 question source](https://github.com/gunqiuwang/cae-question-bank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Feishu-compatible Markdown text with optional JSON export data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local assessment history, wrong-answer records, tested-point tracking, current-test state, recent-question archives, and export JSON files under ./english-assessment when used.] <br>

## Skill Version(s): <br>
4.16.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
