## Description:

Use when auditing garage door safety, planning spring/opener maintenance, or after a door fails to reverse, jams, or drops — CPSC-injury-class hazard audit, auto-reverse 2x4 test protocol, spring cycle-life math with replace-by dates, and service-now verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Homeowners, renters, and household safety planners can use the agent to run and log garage-door safety checks, identify conditions that need professional service, and estimate spring replacement timing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Status output can be mistaken for proof that a door is safe; resolved failures may remain listed, while untested doors can show no open issues.

Mitigation: Check actual test history and perform current physical checks; use the tool as a recordkeeping aid, not a safety certification.

Risk: Generic test or adjustment advice may not match the opener or its instructions.

Mitigation: Follow the opener manufacturer's manual. For reversal tests, use the manufacturer's specified method; Chamberlain's guidance specifies a board rather than a towel.

Risk: Spring cycle-life dates are estimates and do not establish that a spring or door is safe.

Mitigation: Use the dates for maintenance planning, and leave spring, cable, and off-track door repairs to a qualified technician.

## Reference(s):

- [Safety and Springs Reference](references/safety-and-springs.md)
- [Chamberlain safety reversal testing guidance](https://support.chamberlaingroup.com/s/article/How-do-I-test-the-Safety-Reversal-System-1484145519301)
- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/garage-door-safety-audit)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, JSON]

**Output Format:** [Markdown guidance and shell commands, with JSON audit registry and status data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local per-door audit and test history with spring-cycle estimates and service recommendations.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
