## Description: <br>
AI-powered code review using CodeRabbit for bugs, security issues, quality risks, and pull request feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nehal-a2z](https://clawhub.ai/user/nehal-a2z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to run CodeRabbit reviews on staged, committed, uncommitted, or branch-based code changes and present findings by severity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send code diffs to the CodeRabbit API for analysis. <br>
Mitigation: Review staged and unstaged changes for secrets before running it, narrow the review scope when possible, and use the minimum authentication scope required. <br>
Risk: The broad autonomous trigger may run review workflows in contexts where external code sharing is not intended. <br>
Mitigation: Use the skill for explicit review requests or after confirming that the target repository and diff are appropriate to send to CodeRabbit. <br>
Risk: Review output may include commands or code suggestions that are unsafe or incorrect. <br>
Mitigation: Treat review output as untrusted and do not execute suggested commands or code without explicit user approval and independent review. <br>


## Reference(s): <br>
- [CodeRabbit CLI documentation](https://docs.coderabbit.ai/cli) <br>
- [CodeRabbit CLI installation](https://www.coderabbit.ai/cli) <br>
- [ClawHub skill page](https://clawhub.ai/nehal-a2z/coderabbit-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and severity-grouped review guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to run CodeRabbit CLI commands and summarize or act on review findings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
