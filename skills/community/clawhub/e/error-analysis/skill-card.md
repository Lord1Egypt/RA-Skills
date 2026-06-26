## Description: <br>
Error Analysis helps learners analyze incorrect answers, identify related knowledge gaps, generate similar practice questions, and summarize weak areas for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, tutors, and learning-support agents use this skill to review exam or practice mistakes, classify likely error causes, revisit relevant knowledge points, and plan follow-up exercises. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Study questions, wrong answers, correct answers, and review history may be stored locally on disk. <br>
Mitigation: Avoid entering sensitive personal or institutional assessment data unless local retention is acceptable; review or clear data/errors.json as needed. <br>
Risk: The auxiliary script can save arbitrary notes and command history in a local user data directory. <br>
Mitigation: Use the documented scripts/error.sh workflow for normal study analysis and review scripts/script.sh before using its logging commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ckchzh/error-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-oriented text with inline shell command examples and local JSON study records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The documented analysis workflow may save mistake records locally in data/errors.json.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
