## Description:

Tracks express logistics status and delivery history through JisuAPI, including automatic courier recognition and courier-specific validation when required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check package tracking status, signature state, and recent logistics events from an agent workflow. It is useful when a user provides a tracking number and optionally a courier code or phone-number suffix needed by specific couriers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shipment tracking numbers, courier type, the JisuAPI key, and sometimes the last four phone digits are sent to JisuAPI.

Mitigation: Use the skill only when that third-party sharing is acceptable, and avoid sensitive shipments unless the data-sharing terms are approved.

Risk: User-provided tracking details could be mishandled if inserted directly into a shell command.

Mitigation: Pass request data as structured JSON and apply strict quoting or escaping whenever a shell invocation is unavoidable.

Risk: The skill depends on a configured JISU_API_KEY and network access to JisuAPI.

Mitigation: Configure the API key in the environment and handle API, quota, HTTP, and JSON parsing errors before presenting results to users.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jisuapi/skills/express)
- [JisuAPI express API documentation](https://www.jisuapi.com/api/express)
- [JisuAPI website](https://www.jisuapi.com/)
- [JisuAPI express query endpoint](https://api.jisuapi.com/express/query)
- [JisuAPI express type endpoint](https://api.jisuapi.com/express/type)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON from a Python CLI, with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; query input includes a tracking number, optional courier type, and optional phone-number suffix.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
