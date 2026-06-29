## Description: <br>
Detects AI-like writing patterns in Chinese and English long-form articles using six dimensions and returns evidence-backed assessments with improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivian8725118](https://clawhub.ai/user/vivian8725118) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, editors, and reviewers use this skill to evaluate pasted article text or article URLs for AI-like style patterns. It returns a language-aware score table, quoted evidence, a probable-origin judgment, and concrete revision suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-authorship judgments are heuristic and can be mistaken or over-interpreted. <br>
Mitigation: Treat results as writing feedback, not as proof of authorship for academic, employment, moderation, or disciplinary decisions. <br>
Risk: Article URL analysis may access private drafts, internal pages, or authenticated content if a user provides those links. <br>
Mitigation: Submit only text or URLs that the user intends the agent to access and analyze. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vivian8725118/detect-ai-flavor) <br>
- [Evaluation examples](references/evaluation-examples.md) <br>
- [Indicator checklist](references/indicator-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with language detection, a dimension score table, quoted evidence, probable origin, and improvement suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports multi-article comparison tables when the user provides more than one article.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
