## Description:

Advocatus gives an agent a formal adversarial-review role for recording opposition to doctrines, skills, rules, and assumptions before they harden into agency practice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ironiclawdoctor-design](https://clawhub.ai/user/ironiclawdoctor-design)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use Advocatus to create and maintain steelmanned opposition entries, review docket status, and identify assumptions or doctrines that have not survived adversarial challenge. It is for critique capture and review support, not final decision-making.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may cause adversarial critique behavior to appear in shared workflows where it is not desired.

Mitigation: Review and narrow the trigger phrases and standing orders before enabling the skill in shared or production workflows.

Risk: Persistent local opposition records may retain sensitive critiques of internal doctrines, rules, or assumptions.

Mitigation: Use the skill only in appropriate workspaces and review registry and results files before sharing them outside the intended audience.

Risk: The skill records opposition and docket status but does not resolve decisions.

Mitigation: Route final decisions through the normal review process after considering the recorded opposition.

## Reference(s):

- [Opposition Registry](references/opposition-registry.md)
- [Advocatus ClawHub Skill Page](https://clawhub.ai/ironiclawdoctor-design/skills/advocatus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON docket status files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local opposition registry and results files when the included evaluation script is run.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
