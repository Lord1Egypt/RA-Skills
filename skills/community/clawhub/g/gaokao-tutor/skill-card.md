## Description: <br>
High school exam tutor for Chinese Gaokao students that supports guided problem solving, knowledge lookup, practice generation, mistake tracking, essay feedback, study planning, college-major guidance, and emotional support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students preparing for China's Gaokao use this skill for subject tutoring, Socratic step-by-step problem solving, practice generation, essay review, study planning, mistake review, and college application reference guidance. It can also provide brief supportive responses when study stress or distress language appears. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores student learning profile and mistake-history data locally, which can include education records and personal study context. <br>
Mitigation: Require explicit consent before memory features are used, keep storage local, and provide clear view and delete controls for profile and mistake-history files. <br>
Risk: College admission estimates and province policy guidance may be outdated or incomplete because the artifact uses static score and policy data. <br>
Mitigation: Treat admissions guidance as reference only and direct users to verify final decisions against current provincial exam authority notices, official score tables, and university admissions materials. <br>
Risk: The skill handles severe student distress language but evidence.security says crisis-safety safeguards are insufficient. <br>
Mitigation: Add crisis-response instructions that direct self-harm or immediate-danger messages to trusted adults, local emergency services, or qualified human support instead of continuing tutoring. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fangwei-frank/gaokao-tutor) <br>
- [Solving Guide](artifact/references/solving-guide.md) <br>
- [Subject Knowledge Tree](artifact/references/subject-knowledge-tree.md) <br>
- [Question Generator](artifact/references/question-generator.md) <br>
- [Mistakes Guide](artifact/references/mistakes-guide.md) <br>
- [Essay Rubric](artifact/references/essay-rubric.md) <br>
- [Study Plan Template](artifact/references/study-plan-template.md) <br>
- [College Guide](artifact/references/college-guide.md) <br>
- [Province Policy](artifact/references/province-policy.md) <br>
- [Emotional Support Guide](artifact/references/emotional-support.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Conversational Markdown and text, with optional shell commands and JSON-backed local study records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local Gaokao profile and mistake-history memory files when memory features are used.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
