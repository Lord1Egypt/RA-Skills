## Description:

ClawGuard-Auditor helps agents review OpenClaw skills before installation by scanning local skill files for static code patterns, dependency signals, and declared-versus-observed behavior drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stardreaming](https://clawhub.ai/user/stardreaming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to perform a lightweight pre-install review of OpenClaw skills and repositories. It produces findings and risk-tier recommendations that should support, not replace, manual security review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may overstate how much protection its heuristic checks provide.

Mitigation: Treat clean or approving results as advisory only, and require manual review or a stronger contained scanner before installing unfamiliar skills.

Risk: The CLI scans local target directories and reads skill files, code files, package metadata, and code blocks in SKILL.md.

Mitigation: Run it with the narrowest intended target path in a limited workspace, especially when reviewing untrusted or high-risk skills.

Risk: Auto-approval or low-risk language could create false confidence for large or complex targets.

Mitigation: Escalate large, unfamiliar, or security-sensitive targets to human review even when the reported tier is low.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stardreaming/skills/clawguard-auditor)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Terminal text summaries, optional JSON report files, and Markdown-style audit guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk tiers TIER_0 through TIER_4 with process exit codes 0-3 when run through the CLI.]

## Skill Version(s):

3.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
