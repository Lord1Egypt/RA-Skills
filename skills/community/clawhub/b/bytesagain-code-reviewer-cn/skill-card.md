## Description:

Review code files for bugs, security issues, style problems, language-specific checklist items, and complexity signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before commits, during pull request review, onboarding, or codebase audits to run lightweight local checks across Python, JavaScript, Go, Java, and Bash files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could get false confidence from broken advertised security, checklist, or complexity behavior.

Mitigation: Treat the skill as a lightweight local review aid, verify findings manually, and do not use its checks as release gates until the defects are fixed and tested.

Risk: Pattern-based review output can miss issues or flag benign code.

Mitigation: Use the output as a prompt for human review and supplement it with established linters, tests, and security scanners.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-code-reviewer-cn)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text with checklist-style review findings and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local pattern-based checks; manual verification is recommended for failures and release decisions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
