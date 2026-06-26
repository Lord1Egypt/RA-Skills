## Description: <br>
Java code review helper that analyzes Git changes with call-chain context, infers business requirements, scores quality, and generates PRD and review artifacts with checks for Java, Spring, MyBatis, transactions, SQL, performance, concurrency, null safety, and API design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qfann](https://clawhub.ai/user/qfann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering reviewers use this skill to inspect Java repository changes, understand business impact through call-chain analysis, identify implementation risks, and produce structured review and PRD documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read project code and create Markdown review artifacts in a repository. <br>
Mitigation: Invoke it deliberately with the target repository, branch or diff range, and desired output mode; review generated Markdown before committing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qfann/deep-java-review) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown review reports and PRD documents with console summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write code-review-report.md and prd-{version}.md when the user requests file output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
