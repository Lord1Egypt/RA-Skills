## Description: <br>
AI-powered code review assistant that performs static analysis, identifies security vulnerabilities, enforces coding standards, suggests refactoring patterns, and generates PR review comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, tech leads, security engineers, and open source maintainers use this skill to review code snippets, files, diffs, and pull requests for bugs, security issues, performance problems, style violations, and concrete remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad code-review phrases and receive sensitive or proprietary code in the agent context. <br>
Mitigation: Use clear prompts for intended reviews and avoid sharing proprietary code, secrets, or sensitive data unless that exposure is acceptable. <br>
Risk: Generated review findings and suggested fixes may be incomplete or incorrect. <br>
Mitigation: Treat the output as review assistance; require human review, tests, and security validation before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gechengling/ai-code-review-expert) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown review findings with severity labels, code blocks, quality scoring tables, PR summary text, and optional CI/CD guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include proposed fixes, review comments, checklists, and implementation notes; submitted code should be treated as sensitive.] <br>

## Skill Version(s): <br>
3.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
