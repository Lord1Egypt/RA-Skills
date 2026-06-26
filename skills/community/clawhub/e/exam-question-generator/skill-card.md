## Description: <br>
Reads a knowledge map, generates three differentiated practice exam sets, writes structured questions, and renders a standalone HTML review file with answers and explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoucha833-lang](https://clawhub.ai/user/zhoucha833-lang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and exam-preparation users use this skill to turn a prior knowledge map into three practice exams: basic reinforcement, integrated ability, and final simulation. The generated HTML output supports self-review with answers, explanations, scoring, and next-step study guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated practice questions may include incorrect or misleading content from broad prompts or weak source material. <br>
Mitigation: Review the generated questions, answers, and explanations before using them for study or sharing them with others. <br>
Risk: Sensitive study notes can appear in generated question files and HTML output. <br>
Mitigation: Avoid using sensitive source notes unless they are appropriate to include in local generated outputs. <br>
Risk: Regenerating questions can replace earlier generated question files. <br>
Mitigation: Keep a separate copy of any generated exam output that must be preserved before asking the skill to regenerate questions. <br>


## Reference(s): <br>
- [Difficulty Rules](artifact/references/difficulty-rules.md) <br>
- [Question Formats](artifact/references/question-formats.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhoucha833-lang/exam-question-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON and standalone HTML with a short plain-text follow-up prompt] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes .exam-session/questions.json and an exam-questions-YYYYMMDD.html file; reruns can replace earlier generated question outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
