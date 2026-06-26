## Description: <br>
Runs a Chinese CCA practice quiz with 12 scenario-based multiple-choice questions covering five core domains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sawzhang](https://clawhub.ai/user/sawzhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners and developers use this skill to assess CCA readiness through an interactive Chinese mock exam. The agent asks one question at a time, explains answers, scores the full quiz, and recommends domain-specific follow-up study. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares Read and Bash permissions even though the quiz behavior does not require filesystem or shell access. <br>
Mitigation: Install in stricter environments only after reviewing permissions, or prefer a version without Read and Bash access. <br>
Risk: Quiz content and scoring may not reflect the current CCA exam if the exam changes. <br>
Mitigation: Treat results as practice guidance and review answers against current exam objectives before relying on them for readiness decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sawzhang/cca-quiz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted interactive quiz questions, answer explanations, score summaries, and study recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one question at a time and summarizes results after all 12 questions are answered.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
