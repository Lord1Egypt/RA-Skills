## Description: <br>
Bloom Tutor helps an agent run an adaptive Chinese-language Socratic tutoring workflow that creates a syllabus, one lesson document at a time, feedback-driven follow-up lessons, learning logs, and an automatic final summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-evan](https://clawhub.ai/user/li-evan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners use this skill with an agent to open and progress through a topic as an adaptive Chinese-language course. It generates lesson documents, checks feedback and inline questions, updates course progress, keeps a learning log, and creates the final course summary only after the assessment flow is complete. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and updates course files, appends learning-log.jsonl, and scans local course folders for learning progress. <br>
Mitigation: Use it in a workspace intended for learning materials, and review generated or changed files before relying on them. <br>
Risk: The skill uses a temporary pre-summary.md file and the evidence notes that the runtime instructions say not to mention it to the user before deletion. <br>
Mitigation: Avoid using it in workspaces with sensitive notes unless you are prepared to inspect generated course folders and intermediate files yourself. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/li-evan/bloom-tutor) <br>
- [Articles and Tutor Principles](references/articles.md) <br>
- [Learning Log Rules](references/logging.md) <br>
- [Summary Workflow](references/summary.md) <br>
- [Syllabus Rules](references/syllabus.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Chinese-language Markdown course files, syllabus and summary Markdown, JSONL learning-log entries, and concise conversational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates course folders, syllabus and lesson files, summary files, and learning-log.jsonl in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
