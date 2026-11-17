## Description:

Looks up address data for a Brazilian CEP using the ViaCEP API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guilherme-funchal](https://clawhub.ai/user/guilherme-funchal)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Brazilian postal-code address details from a CEP in conversational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CEP queries are sent to ViaCEP over the network, so postal-code lookups leave the local environment.

Mitigation: Use only CEP queries appropriate for the deployment context and confirm network access to ViaCEP is acceptable.

Risk: npm will resolve axios dynamically because the artifact does not include a lockfile.

Mitigation: Install in an isolated OpenClaw environment and ask the publisher to pin dependencies and include a lockfile for reproducible installs.

## Reference(s):

- [ViaCEP API](https://viacep.com.br)
- [axios package](https://www.npmjs.com/package/axios)
- [ClawHub skill page](https://clawhub.ai/guilherme-funchal/skills/cep-lookup)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text address summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns street, neighborhood, city, state, and complement when available; reports invalid CEP, not found, or network errors.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
