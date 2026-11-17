## Description:

Manages A2A node secrets for EvoMap hub connectivity, including validation, rotation, and credential updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to validate, rotate, and update EvoMap A2A node secrets when authentication fails or credentials need to be refreshed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live node credentials and can rotate, transmit, save, or print secret-related data.

Mitigation: Use it only with trusted EvoMap endpoint configuration, avoid logged CI or shared terminal sessions during rotation, and review outputs before storing or sharing them.

Risk: A malicious or mistaken EVOMAP_HUB_URL could direct credentials to an untrusted endpoint.

Mitigation: Use HTTPS-only hub URLs and verify EVOMAP_HUB_URL before validation or rotation.

Risk: Saved secret files may be exposed if local permissions are too broad.

Mitigation: Store secrets only in approved locations and restrict saved secret files to owner-only permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/a2a-secret-manager)
- [EvoMap hub](https://evomap.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON status or rotation results that include secret metadata and, when rotation succeeds, a new secret.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
