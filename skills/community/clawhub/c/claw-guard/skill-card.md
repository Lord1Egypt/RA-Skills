## Description:

Security auditor for ClawHub skills that scans SKILL.md and scripts for prompt injection, data exfiltration, shell injection, permission mismatches, and malicious patterns, then returns a PASS, WARN, or FAIL verdict with a breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taha2053](https://clawhub.ai/user/taha2053)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use ClawGuard to inspect ClawHub skills before installation or in CI workflows. It produces local audit findings so users can decide whether a skill needs review or should be blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat a PASS verdict as a definitive safety approval even though the server security summary says the scanner is heuristic and can miss issues.

Mitigation: Use ClawGuard as one review input and require manual inspection or additional security checks before installing or releasing a skill.

Risk: The server security guidance notes that the packaged script path should be corrected or verified before use.

Mitigation: Confirm the installed file layout and command path in the target ClawHub environment before relying on CLI or CI invocations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taha2053/skills/claw-guard)
- [Publisher profile](https://clawhub.ai/user/taha2053)
- [Project homepage](https://github.com/Taha2053/clawguard)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown report or JSON summary with verdicts, checks, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI supports single-skill scans, bulk scans, JSON output, and optional failure on warnings.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
