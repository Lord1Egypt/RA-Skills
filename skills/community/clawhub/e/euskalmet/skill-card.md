## Description:

Tool for obtaining weather forecasts for the Basque Country through the Euskalmet agency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero-astro](https://clawhub.ai/user/zero-astro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve Euskalmet weather forecasts for Basque Country locations and present current conditions, temperatures, and short-range trends in Basque.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A diagnostic script can print a prefix of the Euskalmet private key when run in a logged environment.

Mitigation: Do not run scripts/test_env.py where logs are shared; rotate the private key if any prefix has already been exposed.

Risk: Dependencies are stale or not fully locked.

Mitigation: Review, update, and pin dependencies before deployment.

## Reference(s):

- [Euskalmet](https://www.euskalmet.euskadi.eus/)
- [ClawHub skill page](https://clawhub.ai/zero-astro/skills/euskalmet)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Basque-language Markdown text plus forecast JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Euskalmet API email and private key environment variables; optional greeting name customizes the formatted message.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
