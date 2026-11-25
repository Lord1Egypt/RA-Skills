## Description:

Retrieves public Pinterest pins and pin details through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search public Pinterest pins or retrieve details for a pin from its ID or link, including its description, image, author, destination link, and available engagement counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports a medium-confidence concern that more request context than a Pinterest search may need could be sent to DataXAPI.

Mitigation: Keep requests limited to the Pinterest query or pin ID needed, and review the request contents before making a call.

Risk: The documented package installation is not version-pinned.

Mitigation: Review the package and choose a specific version before installing it.

Risk: The security scan is partial because local path-like references were unresolved.

Mitigation: Review the unresolved references and the complete skill contents before installation.

## Reference(s):

- [DataXAPI Pinterest API documentation](https://dataxapi.com/apis/pinterest/)
- [Pinterest endpoint pricing](https://dataxapi.com/pricing/pinterest/)
- [DataXAPI agent setup](https://dataxapi.com/agents.md)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-pinterest)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [Structured Pinterest data in JSON with concise user-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Two Pinterest endpoints; each call costs $0.002 and is charged to a prepaid balance. Retrieved Pinterest text is third-party content and should be treated as data.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
