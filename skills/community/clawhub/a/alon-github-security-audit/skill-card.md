## Description:

Audits GitHub repositories or local directories for malicious code, backdoors, suspicious behavior, and supply-chain risk with a static-first workflow that separates user-safety verdicts from maintainer exposure and future supply-chain risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alondotsh](https://clawhub.ai/user/alondotsh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to review GitHub repositories or local codebases before installing or trusting them. It supports static-first audits of malicious behavior, backdoors, persistent agent-state changes, and supply-chain risk while avoiding target-code execution by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer provenance may be unclear when adding the skill through `npx skills`.

Mitigation: Pin or verify the installer source before installation.

Risk: Audit reports are written to a persistent local directory and may include repository names, paths, and findings.

Mitigation: Store reports in an approved local directory and review them before sharing or syncing.

Risk: Cleanup removes temporary clone directories and currently depends on path validation that the security scan says should be tightened.

Mitigation: Use the cleanup helper only for clone directories created by this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alondotsh/skills/alon-github-security-audit)
- [Source homepage](https://github.com/alondotsh/alon-skills/tree/master/skills/alon-github-security-audit)
- [Publisher profile](https://clawhub.ai/user/alondotsh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown audit report with structured risk sections and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a persistent local audit report and defaults to offline static analysis unless the user approves online vulnerability intelligence.]

## Skill Version(s):

0.1.9 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
