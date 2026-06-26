## Description: <br>
评估文章、作业、公众号稿、报告、评论、邮件或任意文本的 AI 写作、AI 辅助润色、人机混写或模板化写作风险，并输出证据化、克制、非定罪式判断。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacktian89](https://clawhub.ai/user/zacktian89) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, editors, reviewers, and content teams use this skill to review supplied text for AI-writing, AI-assisted polishing, human-AI mixed writing, or template-like writing risk. It emphasizes evidence strength, sample limits, alternative explanations, and follow-up evidence rather than treating detector-style signals as proof. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat a heuristic AI-writing risk assessment as proof of misconduct or authorship. <br>
Mitigation: Use the output only as one review signal and require additional evidence, such as drafts, revision history, sources, author baseline text, or human review for academic, employment, legal, copyright, or disciplinary decisions. <br>
Risk: Short, translated, heavily edited, collaborative, or highly templated text can make AI-writing judgments unreliable. <br>
Mitigation: State sample limitations, evidence strength, and alternative explanations before assigning a risk level or score. <br>
Risk: Revision advice could be misused as detector-evasion guidance. <br>
Mitigation: Frame suggestions around authentic expression, source traceability, concrete detail, and information density, and avoid instructions for bypassing AI detectors. <br>


## Reference(s): <br>
- [AI Detection Methods](references/ai-detection-methods.md) <br>
- [Evaluation Template](references/evaluation-template.md) <br>
- [ClawHub Release Page](https://clawhub.ai/zacktian89/ai-writing-risk-review) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown report, Chinese by default unless the user requests another language] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces heuristic risk ratings and evidence-ranked review guidance; it does not execute tools, access external data, or persist information.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
