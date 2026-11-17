## Description:

Agent wellness and maintenance suite for memory cleanup, security scanning, prompt injection detection, alignment adjustment, skills auditing, and health diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whooshinglander](https://clawhub.ai/user/whooshinglander)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent operators use ClawSpa to inspect local agent memory, installed skills, instruction alignment, configuration health, and prompt-injection residue before approving cleanup or remediation changes. The skill is primarily local-first, with optional cloud analysis documented separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect private agent memory, profile files, instruction files, installed skills, scheduler settings, and possible plaintext secrets.

Mitigation: Require explicit confirmation of the scan scope before running and keep the default local-first mode unless the user has reviewed external privacy terms.

Risk: Generated cleanup, remediation, uninstall, or alignment recommendations could affect persistent agent behavior if applied without review.

Mitigation: Treat findings as proposals and require explicit user approval before modifying, deleting, uninstalling, or rewriting any files or skills.

Risk: Persistent ClawSpa state, report paths, and HEARTBEAT.md weekly scheduling may create ongoing maintenance behavior that the user did not intend.

Mitigation: Confirm the exact report destination, ~/.openclaw/clawspa state, and any HEARTBEAT.md schedule before creating or enabling them.

Risk: Optional cloud analysis could disclose agent metadata or sensitive context if enabled without review.

Mitigation: Run local scans first and review clawspa.org documentation and privacy details before enabling any cloud analysis.

## Reference(s):

- [ClawSpa website](https://clawspa.org)
- [ClawSpa documentation](https://clawspa.org/docs)
- [ClawSpa privacy details](https://clawspa.org/docs#what-we-send)
- [Where Am I Burning Tokens?](https://clawhub.ai/whooshinglander/whereamiburningtokens)
- [Cloud Analysis Note](references/api-integration.md)
- [Deep Cleanse - Full Procedure](references/deep-cleanse.md)
- [Security Scan - Full Procedure](references/security-scan.md)
- [Detox - Full Procedure](references/detox.md)
- [Alignment Adjustment - Full Procedure](references/alignment-adjustment.md)
- [Declutter - Full Procedure](references/declutter.md)
- [Health Report - Full Procedure](references/health-report.md)
- [Token Diet - Add-on Treatment](references/token-diet.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, scan findings, cleanup proposals, configuration guidance, and approval-gated shell or file-operation recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local reports may be saved under memory/spa-reports; proposed changes require explicit user approval before modification, deletion, uninstall, or scheduling.]

## Skill Version(s):

1.4.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
