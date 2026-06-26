## Description: <br>
Grades higher-mathematics subjective responses from image, LaTeX, or text inputs, checks calculus reasoning, and generates step-level feedback for teacher review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daigxok](https://clawhub.ai/user/daigxok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Instructors, teaching assistants, and education developers use this skill to evaluate calculus homework, proof attempts, and worked solutions, then produce step scores, error explanations, and multimodal feedback. It is best used with human review when real student work or final grades are involved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process identifiable student submissions through external OCR or LLM providers. <br>
Mitigation: Use only approved providers, avoid identifiable submissions where possible, and define consent, retention, deletion, access control, and cache handling before classroom or institutional deployment. <br>
Risk: Automated grading and feedback can be incorrect or misleading for high-stakes assessment. <br>
Mitigation: Require teacher or teaching-assistant review for final scores, rubric alignment, and feedback sent to students. <br>
Risk: Cached grading data can retain sensitive student work longer than intended. <br>
Mitigation: Configure cache retention limits, restrict access to stored submissions and results, and delete cached records according to the institution's policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daigxok/calculus-intelligent-grading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON results and Markdown-style guidance with example shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include step-level scores, error categories, text annotations, voice feedback references, recommended learning resources, and proof-structure analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
