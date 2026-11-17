## Description:

aispeech_ainote helps OpenClaw agents access AISpeech office-product notes, todos, personal database search, tag knowledge bases, and hotword APIs for AI office tablets and recording cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fairylong](https://clawhub.ai/user/fairylong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw agents use this skill to read, search, create, update, and delete AISpeech office notes and todos, synchronize tag knowledge bases, and manage hotwords through authenticated AIWorks APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived bearer token can grant sensitive read, write, and delete access to notes, todos, labels, personal database search, and hotwords.

Mitigation: Use skill-scoped secret injection for AIWORK_AUTH_TOKEN, grant only the scopes needed for the intended workflow, and avoid gateway-global environment variables or plaintext backup files where possible.

Risk: A changed or incorrect service endpoint could expose the bearer token or route requests to an unintended service.

Mitigation: Keep AIWORK_BASE_URL on the official HTTPS origin unless the publisher and operator have explicitly validated an alternate endpoint.

Risk: Write and delete APIs can modify or remove user notes, groups, todos, labels, or hotwords.

Mitigation: Require explicit user confirmation before delete, move, bind, sync, create, or update operations that affect user data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fairylong/skills/aitablet)
- [AIWorks service origin](https://aiworks.cn)
- [API reference](api_reference.md)
- [API details](references/api-details.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Configuration]

**Output Format:** [Markdown guidance with HTTP API details, JSON request and response bodies, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIWORK_AUTH_TOKEN; AIWORK_BASE_URL is optional and defaults to https://aiworks.cn.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
