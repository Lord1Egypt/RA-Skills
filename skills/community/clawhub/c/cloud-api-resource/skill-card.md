## Description:

Helps an agent collect parameters, confirm user intent, sign UCloud API requests, and create UCloud resources such as UHost instances, API keys, UFile buckets, databases, and VPCs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[892577738-bot](https://clawhub.ai/user/892577738-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent guide UCloud resource creation, gather required API parameters, request final confirmation, execute UCloud API calls, and return resource identifiers or error details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create live UCloud resources after user confirmation, which may incur cost or change cloud infrastructure.

Mitigation: Review the proposed configuration carefully before confirming any creation request and use credentials scoped only to the intended project and operations.

Risk: The skill handles cloud API credentials, including private keys used for request signing.

Mitigation: Use a restricted sub-account key, avoid broad account keys in chat or ordinary tool arguments, and rotate credentials after testing.

Risk: Caller-provided API URLs could direct signed requests to an unexpected endpoint.

Mitigation: Fix or validate the endpoint against the real UCloud API host before signing and sending requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/892577738-bot/skills/cloud-api-resource)
- [UCloud CreateUHostInstance API endpoint example](https://api.ucloud.cn/?Action=CreateUHostInstance)
- [UCloud CreateUMInferAPIKey API endpoint example](https://api.ucloud.cn/?Action=CreateUMInferAPIKey)
- [UCloud CreateBucket API endpoint example](https://api.ucloud.cn/?Action=CreateBucket)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance plus JSON-like API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, HTTP status code, raw response data, extracted resource IDs when available, and error messages on failure.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
