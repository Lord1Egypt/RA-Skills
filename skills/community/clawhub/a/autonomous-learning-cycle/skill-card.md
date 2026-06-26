## Description: <br>
Autonomous Learning Cycle schedules a recurring agent workflow that selects tasks, extracts reusable patterns, scores confidence, generates skills, and produces daily or weekly reflection outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, learners, and project managers use this skill to run a self-improvement loop that records learning patterns, creates follow-up tasks, generates reflection reports, and proposes reusable skills. It is intended for users who explicitly want persistent autonomous learning automation in a controlled workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables persistent scheduled automation that can continue running without close supervision. <br>
Mitigation: Enable it only after reviewing the scheduled jobs, run it in a contained workspace, and confirm how to disable or remove all scheduled jobs. <br>
Risk: The skill writes tasks, learning records, reflection reports, and generated skill files that may affect future agent behavior. <br>
Mitigation: Require manual review before accepting generated tasks or using generated skills, and keep generated files under version control or another review process. <br>
Risk: The skill performs shell-based external discovery during learning-direction generation. <br>
Mitigation: Inspect or disable external discovery commands before enabling the workflow, especially in environments with sensitive data or network restrictions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/autonomous-learning-cycle) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON and JSONL records, generated skill files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recurring workspace artifacts such as task queues, confidence records, reflection reports, and generated skill drafts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact package metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
