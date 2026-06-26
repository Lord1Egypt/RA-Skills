## Description: <br>
Combines C++ static analysis, AI-assisted review, iterative multi-reviewer feedback, C++-specific checks, scoring, and optional fixes for pull requests, diffs, files, and full projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bigmasteryy](https://clawhub.ai/user/bigmasteryy) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to review C and C++ code for memory safety, undefined behavior, security issues, performance concerns, maintainability, and modern C++ practices before merge or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read repository source code and can use AI-backed review flows. <br>
Mitigation: Use local-only mode for sensitive or regulated repositories and review any dependent paid or API-backed reviewer skills before enabling them. <br>
Risk: Optional auto-fix behavior can modify project files. <br>
Mitigation: Keep auto-fix disabled unless the repository is under version control, require user confirmation before fixes, and inspect the resulting diff before committing. <br>
Risk: Review scores and findings can be subjective or incomplete. <br>
Mitigation: Treat generated reports as review assistance, prioritize manual validation for high-severity findings, and tune rules to the project context. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bigmasteryy/cpp-code-review-master) <br>
- [Publisher Profile](https://clawhub.ai/user/bigmasteryy) <br>
- [C++ Review Workflow](references/workflow.md) <br>
- [C++ Review Checklist](references/cpp-checklist.md) <br>
- [Severity Definitions](references/severity.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with issue tables, severity ratings, scores, prioritized fixes, and optional code or shell command suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May inspect files, diffs, or pull requests; optional fixes should be applied only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
