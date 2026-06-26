## Description: <br>
Summarize a person's git commits on a given date, grouped by feature area with concise descriptions for daily work review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrew020](https://clawhub.ai/user/andrew020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering managers use this skill to review a person's daily git commits by date, grouped into feature or functional areas with concise English summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commit messages, author names, and file paths from local git history can be summarized into chat. <br>
Mitigation: Run the skill only in repositories where that history is acceptable to expose, and avoid repositories with sensitive commit metadata. <br>
Risk: The summary depends on git log filters and the quality of commit messages and file paths. <br>
Mitigation: Review the generated summary against the listed commit hashes before using it as a daily work record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andrew020/daily-commits) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown daily commit summary with grouped bullet lists and a total commit count] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [English-only summary; omits merge commits; states clearly when no commits are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
