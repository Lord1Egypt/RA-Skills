## Description:

Runs a two-pass multidisciplinary code audit across security, performance, UX, DX, and edge cases, producing one prioritized report with concrete fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[swader](https://clawhub.ai/user/swader)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to audit repositories, pull requests, product flows, and infrastructure scripts for security, performance, UX, DX, and edge-case risks. The skill is intended to produce a prioritized remediation plan with evidence, concrete fixes, and verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled sync script can overwrite or delete user-writable agent skill directories with weak path guardrails.

Mitigation: Review the skill before installing, prefer the platform's normal reviewed install flow, and expect the script to modify persistent agent skill directories.

Risk: Untrusted --skill-name or --source values can steer the sync script toward unintended persistent locations.

Mitigation: Run the sync script only with trusted arguments and inspect destination paths before use.

Risk: Unpinned npx execution during optional installation can fetch changing installer behavior.

Mitigation: Avoid unpinned npx execution for reviewed installs, or pin and review the installer version before running it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/swader/skills/agent-skills-audit)
- [Audit Framework](references/audit-framework.md)
- [Claude Agent Skills Documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Cursor Skills Documentation](https://cursor.com/docs/context/skills)
- [Open Skills Installer](https://github.com/vercel-labs/skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings first, followed by open questions, remediation plan, verification plan, and executive summary.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
