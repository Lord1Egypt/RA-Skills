## Description: <br>
ClawSpa helps OpenClaw agents run local maintenance sessions for memory cleanup, security scanning, prompt-injection checks, alignment review, skill decluttering, and health reporting, with optional cloud analysis documented separately. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whooshinglander](https://clawhub.ai/user/whooshinglander) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent maintainers use ClawSpa to audit memory, installed skills, configuration, and prompt-injection residue, then receive reports and cleanup proposals that require explicit approval before changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect sensitive local agent memory, installed skills, configuration, and recent logs. <br>
Mitigation: Install and run it only when local maintenance is intended, and treat generated reports and history as potentially sensitive. <br>
Risk: Cleanup, uninstall, or alignment recommendations could remove useful context or change agent behavior if applied without review. <br>
Mitigation: Require explicit approval before modifications and create backups before any approved file changes. <br>
Risk: Optional cloud or deep analysis may share data with clawspa.org. <br>
Mitigation: Review the clawspa.org docs and privacy details first, and do not send raw memory content or credentials. <br>
Risk: Security and prompt-injection scans are heuristic and may miss issues or produce false positives. <br>
Mitigation: Use findings as review prompts and verify high-risk items before acting on them. <br>


## Reference(s): <br>
- [Deep Cleanse procedure](references/deep-cleanse.md) <br>
- [Security Scan procedure](references/security-scan.md) <br>
- [Detox procedure](references/detox.md) <br>
- [Alignment Adjustment procedure](references/alignment-adjustment.md) <br>
- [Declutter procedure](references/declutter.md) <br>
- [Health Report procedure](references/health-report.md) <br>
- [Cloud Analysis Note](references/api-integration.md) <br>
- [Token Diet add-on](references/token-diet.md) <br>
- [ClawSpa docs](https://clawspa.org/docs) <br>
- [ClawSpa privacy details](https://clawspa.org/docs#what-we-send) <br>
- [Where Am I Burning Tokens?](https://clawhub.ai/whooshinglander/whereamiburningtokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, findings lists, and user-approved shell or file-change instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-first reports may be saved under memory/spa-reports; cleanup, deletion, uninstall, and alignment changes require explicit approval.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
