## Description: <br>
中文文本校验专家，用于全面检查 PPT、Word、Markdown 等文档中的中文错别字、标点符号、格式规范、学术用语、逻辑表达及文档专项问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hntong](https://clawhub.ai/user/hntong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, reviewers, students, researchers, and business users can use this skill to proofread Chinese text in presentations, documents, and Markdown files. It produces a structured review report that highlights issues by location, severity, issue type, and suggested correction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger words may activate the proofreading behavior more often than expected. <br>
Mitigation: Review whether the requested task is a Chinese text proofreading task before applying the skill. <br>
Risk: Documents submitted for proofreading may contain confidential or sensitive content. <br>
Mitigation: Review document sensitivity before providing content to the agent and avoid sharing confidential material unless the deployment environment is approved for it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hntong/chinese-text-proofreader) <br>
- [Publisher profile](https://clawhub.ai/user/hntong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with summary bullets, issue tables, and optional revised text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports issues by document location, original text, issue type, suggested correction, and severity.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
