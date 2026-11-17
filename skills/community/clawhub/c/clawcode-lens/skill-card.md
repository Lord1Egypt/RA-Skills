## Description:

ClawCode Lens helps agents explain source code, run local pattern-based security checks, and produce improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect source files, summarize code structure, identify common risky patterns, and generate prioritized improvement guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release makes local-only privacy claims while the artifact also documents a paid deep-scan path that uploads selected source code externally.

Mitigation: Use the local scripts for confidential or proprietary code, and avoid any remote deep scan unless the publisher clarifies the external API, billing, consent flow, and privacy behavior.

Risk: Pattern-based security checks may miss vulnerabilities or report false positives.

Mitigation: Treat scan results as triage guidance and review findings with standard secure-code review and testing before deployment.

## Reference(s):

- [ClawCode Lens release page](https://clawhub.ai/northcap-group/skills/clawcode-lens)
- [northcap-group publisher profile](https://clawhub.ai/user/northcap-group)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or plain text reports with optional shell commands and code excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to files when invoked with output flags.]

## Skill Version(s):

1.0.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
