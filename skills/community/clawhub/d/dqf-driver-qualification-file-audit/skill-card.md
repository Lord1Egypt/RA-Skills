## Description:

Use this skill when a motor-carrier safety director, DOT compliance manager, or third-party DQF administrator needs a pre-audit review of FMCSA Driver Qualification Files under 49 CFR § 391.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

DOT-regulated motor-carrier safety directors, DOT compliance managers, third-party DQF administrators, and HR safety staff use this skill to conduct draft pre-audit reviews of driver qualification files, prioritize remediation, and prepare DER-reviewed fleet rollups.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Draft findings may be mistaken for official FMCSA submissions, certified compliance records, or legal advice.

Mitigation: Keep outputs labeled as draft pre-audit aids and require DER, compliance counsel, or qualified safety staff review before operational action.

Risk: Driver qualification files may contain sensitive identifiers or medical details.

Mitigation: Avoid pasting full CDL numbers, SSNs, full addresses, or medical details into chat; use internal driver IDs and CDL last-4.

Risk: The agent cannot verify external systems such as Clearinghouse, CDLIS, the FMCSA Portal, the National Registry, TPR, or state DMV databases.

Mitigation: Use the skill to document requirements and draft findings only; authorized carrier staff should perform official system checks outside the agent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/archlab-space/skills/dqf-driver-qualification-file-audit)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft audit packet with per-driver tables, prioritized findings, fleet rollup, immediate-action list, cited-regulation appendix, and DER sign-off block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are draft pre-audit aids for DER and qualified compliance review; use internal driver IDs and CDL last-4 rather than full sensitive identifiers.]

## Skill Version(s):

0.1.1 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
