## Description: <br>
高中学习助手 is a Chinese-language tutoring skill that helps middle and high school students understand subject concepts, work through exercises, and receive teacher-style study guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatif146](https://clawhub.ai/user/whatif146) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and education-support agents use this skill to answer Chinese-language school subject questions, guide step-by-step problem solving, and provide supportive study coaching across common middle and high school subjects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Students or educators may upload private student records, sensitive assignments, or personal documents for tutoring context. <br>
Mitigation: Use non-sensitive study materials where possible and confirm the runtime's storage, retention, and deletion behavior before uploading private documents. <br>
Risk: Broad tutoring triggers may activate the skill for general Chinese-language why, how, or teach-me requests outside the intended study context. <br>
Mitigation: Review activation behavior during deployment and ask the agent to confirm education context when a request is ambiguous. <br>
Risk: The skill provides educational explanations and may make mistakes when reference material is incomplete or outside its built-in subjects. <br>
Mitigation: Have learners verify important answers against class materials, textbooks, or a qualified teacher, especially for exams or graded work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/whatif146/chinese-student-tutor) <br>
- [Publisher profile](https://clawhub.ai/user/whatif146) <br>
- [Clawdis homepage](https://github.com/yooyoo) <br>
- [Teaching tips](artifact/references/teaching-tips.md) <br>
- [Response templates](artifact/references/response-templates.md) <br>
- [Typical problems](artifact/references/exercises/typical-problems.md) <br>
- [Math reference](artifact/references/textbooks/math.md) <br>
- [Physics reference](artifact/references/textbooks/physics.md) <br>
- [Chemistry reference](artifact/references/textbooks/chemistry.md) <br>
- [Chinese reference](artifact/references/textbooks/chinese.md) <br>
- [English reference](artifact/references/textbooks/english.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown responses with structured explanations, quoted reference excerpts, step-by-step tutoring prompts, and practice questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language educational guidance; may ask follow-up questions before providing a full solution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
