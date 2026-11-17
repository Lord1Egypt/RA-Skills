## Description:

Guides evidence-first debugging with temporary probes, reproduction, a minimal root-cause fix, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liush2yuxjtu](https://clawhub.ai/user/liush2yuxjtu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to diagnose reproducible bugs by testing competing hypotheses against runtime evidence before making and verifying a focused fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autopilot can run project commands and tests in the current environment.

Mitigation: Check that project commands and tests are safe before enabling Autopilot.

Risk: Temporary probe logs may contain sensitive data.

Mitigation: Redact secrets and personal data, review logs before sharing, and remove probes and generated logs when finished.

## Reference(s):

- [Debug Mode on ClawHub](https://clawhub.ai/liush2yuxjtu/skills/debug-mode)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands]

**Output Format:** [Markdown with debugging steps, probe suggestions, and a verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Temporary probes and logs are removed after verification.]

## Skill Version(s):

0.1.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
