## Description: <br>
Exam Prep Pro helps users prepare for professional exams by producing study plans, high-frequency concept cards, practice questions, mistake reviews, and final sprint guidance from bundled exam reference materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcheisenberg](https://clawhub.ai/user/mcheisenberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners use this skill to build exam-specific study schedules, review high-yield topics, generate practice questions, analyze missed questions, and prepare for final review across supported professional exams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to complete payment through an external QR-code flow for Pro activation. <br>
Mitigation: Install or use Pro features only if the publisher is trusted and the external payment flow is acceptable for the user's organization or environment. <br>
Risk: Activation may require running a bundled Python verifier. <br>
Mitigation: Review the verifier before execution and run it in an environment where local file writes to the user's home directory are acceptable. <br>
Risk: Successful activation stores the activation code in a hidden file in the user's home directory. <br>
Mitigation: Treat the stored activation marker as sensitive local data and remove it when the skill should no longer remain activated on that machine. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcheisenberg/skills/exam-prep-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/mcheisenberg) <br>
- [Exam Registry](artifact/references/exam_registry.md) <br>
- [CPA Syllabus and Weights](artifact/references/cpa_syllabus.md) <br>
- [CPA High-Frequency Topics](artifact/references/cpa_highfreq.md) <br>
- [Legal Exam Syllabus and Weights](artifact/references/fk_syllabus.md) <br>
- [Legal Exam High-Frequency Topics](artifact/references/fk_highfreq.md) <br>
- [Civil Service Exam Syllabus and Weights](artifact/references/gwy_syllabus.md) <br>
- [Civil Service Exam High-Frequency Topics](artifact/references/gwy_highfreq.md) <br>
- [Teacher Qualification Syllabus and Weights](artifact/references/jszg_syllabus.md) <br>
- [Teacher Qualification High-Frequency Topics](artifact/references/jszg_highfreq.md) <br>
- [Construction Engineer Syllabus and Weights](artifact/references/jzs_syllabus.md) <br>
- [Construction Engineer High-Frequency Topics](artifact/references/jzs_highfreq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown study guidance with occasional inline shell commands for activation verification] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate daily plans, topic cards, practice questions, answer explanations, mistake-remediation prompts, and exam sprint checklists.] <br>

## Skill Version(s): <br>
1.4.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
