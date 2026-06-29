## Description: <br>
AI Code Review guides agents through pull request review, code quality checks, security inspection, performance analysis, and CI/CD status triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to have an agent inspect pull requests or local changes, summarize CI/CD failures, and produce structured code review feedback with concrete remediation suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use GitHub authority for comments, labels, close decisions, proof publication, and corrective commits. <br>
Mitigation: Review the target repository, pull request, proposed comments, and any write actions before allowing the agent to execute GitHub commands. <br>
Risk: Review output may contain incorrect or misleading findings if the agent lacks project context or misreads CI/CD failures. <br>
Mitigation: Validate findings against the code diff, CI logs, and local project checks before publishing or acting on the review. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/terrycarter1985/ai-code-review) <br>
- [Review reference guide](artifact/reference.md) <br>
- [Review examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with structured review sections and inline code or shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CI/CD status summaries, issue severity groupings, review comments, remediation steps, and verification commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
