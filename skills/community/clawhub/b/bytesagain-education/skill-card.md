## Description: <br>
Generate 7-day structured learning plans, quizzes, and local study progress summaries without internet access or an account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Learners and self-directed developers use this skill to generate short study plans, practice quizzes, and progress summaries for technical topics. It is suited to local, account-free learning workflows where generated guidance should be reviewed before relying on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes study progress to a local JSON file under the user's home directory, and reset clears that saved progress. <br>
Mitigation: Avoid storing sensitive information in topic or milestone names, and confirm before using progress reset. <br>
Risk: Generated learning plans and quizzes may be incomplete or inaccurate for a learner's specific goals. <br>
Mitigation: Review the generated plan and quiz content against trusted learning resources before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/bytesagain-education) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands] <br>
**Output Format:** [Terminal text and Markdown-style examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include 7-day plans, quiz questions with answers, and local progress summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
