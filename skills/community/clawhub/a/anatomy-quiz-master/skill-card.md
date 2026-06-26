## Description: <br>
Generates anatomy quiz questions for medical education, with selectable anatomical regions, difficulty labels, answers, explanations, and clinical notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners, medical students, and teaching assistants use this skill to generate supplemental anatomy self-assessment questions, study quizzes, and classroom practice material. It should support, not replace, faculty-reviewed anatomy resources, atlases, and lab instruction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation advertises adaptive learning, image quizzes, and progress tracking that are not implemented in the provided code. <br>
Mitigation: Treat the release as a local static quiz generator unless those missing features are added and reviewed. <br>
Risk: Generated educational content may contain anatomy inaccuracies or omit current terminology. <br>
Mitigation: Review quiz content against faculty-approved anatomy references before using it for assessment or instruction. <br>
Risk: The CLI can write output to a user-specified file path. <br>
Mitigation: Choose output paths deliberately and review commands before execution. <br>


## Reference(s): <br>
- [Anatomy Quiz Master References](artifact/references/guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/anatomy-quiz-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [JSON or plain text quiz content, with Markdown usage guidance and inline shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can print generated questions to stdout or write JSON quiz output to a user-specified file path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
