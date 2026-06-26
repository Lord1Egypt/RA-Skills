## Description: <br>
Comprehensive code review assistant that analyzes code quality, identifies bugs, suggests improvements, and ensures adherence to best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GuoShamin](https://clawhub.ai/user/GuoShamin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests, audit code quality, identify security and performance issues, and produce actionable review feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may suggest Bash commands or review steps that execute project code, modify files, or contact external services. <br>
Mitigation: Review commands before running them and use the skill only with repositories the user is comfortable letting an assistant inspect. <br>
Risk: Review feedback can be incomplete or misleading when repository context, tests, or project standards are missing. <br>
Mitigation: Treat findings as review assistance and confirm material issues against the codebase, tests, and team standards before acting. <br>


## Reference(s): <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>
- [Clean Code Principles](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) <br>
- [Google Style Guides](https://google.github.io/styleguide/) <br>
- [Effective Code Review](https://google.github.io/eng-practices/review/) <br>
- [ClawHub skill page](https://clawhub.ai/GuoShamin/code111) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review comments with code examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity-grouped findings, file and line references, suggested fixes, and test or documentation recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
