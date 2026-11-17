## Description:

Runs the ESR OpenClaw host security check script and presents the complete audit results for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpany37-max](https://clawhub.ai/user/xpany37-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and security reviewers use this skill to run local OpenClaw host checks, view the raw findings, and receive concise remediation guidance before making any configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled DingTalk reporting can send sensitive audit results and host identifiers outside the machine.

Mitigation: Use the manual local check by default; enable the cron and DingTalk workflow only after verifying the recipient group, data handling expectations, and removal plan.

Risk: Generated JSON audit files can expose local security posture and configuration details.

Mitigation: Store results with restricted access, treat them as sensitive local files, and remove or archive them according to the operator's retention policy.

Risk: A reported safe status may not fully prove sandboxing or network exposure is acceptable.

Mitigation: Independently verify sandbox settings, listening addresses, and network exposure before relying on the audit summary.

## Reference(s):

- [README](artifact/README.md)
- [Usage Guide](artifact/USAGE_GUIDE.md)
- [Output Format](artifact/OUTPUT_FORMAT.md)
- [Cron Configuration](artifact/CRON_CONFIG.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown-style agent response with raw command output, concise risk summary, remediation guidance, and timestamped JSON audit files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill is expected to show the script output completely before summarizing risks and to request user confirmation before applying fixes.]

## Skill Version(s):

3.2.1 (source: server release metadata, config.json, and CHANGELOG.md; released 2026-03-16 in artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
