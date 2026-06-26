## Description: <br>
Review code files for bugs, security issues, style problems, complexity hotspots, and language-specific checklist items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before commits, during pull-request review, onboarding, or codebase audits to get pattern-based findings, review checklists, security checks, complexity metrics, and diffs for selected files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan can print matching lines from selected files, which may expose passwords, tokens, API keys, or other sensitive content in the agent session. <br>
Mitigation: Run the skill only on files you intentionally select, and avoid scanning live secrets or credential-bearing configuration unless that exposure is acceptable. <br>
Risk: The review and security checks are pattern-based and may miss issues or produce findings that need human judgment. <br>
Mitigation: Treat output as review assistance, not a substitute for manual review, tests, dedicated security tooling, or project-specific policy checks. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/bytesagain-code-reviewer-cn) <br>
- [Publisher profile](https://clawhub.ai/user/loutai0307-prog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text and checklist-style Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected local files and prints review findings, checklists, security matches, complexity summaries, or unified diffs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
