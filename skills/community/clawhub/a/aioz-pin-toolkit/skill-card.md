## Description:

Respond to user requests for AIOZ Pin API operations using provided scripts to manage API keys, pin files to IPFS, track usage, and inspect pinning resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[namle-aioz](https://clawhub.ai/user/namle-aioz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage AIOZ Pin resources: pin local files or CIDs, inspect and list pins, manage API keys, and retrieve usage or billing data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AIOZ Pin credentials may be exposed if supplied as command-line arguments.

Mitigation: Use secure environment variables or a wrapper before execution; never pass PINNING_API_KEY, PINNING_SECRET_KEY, or AIOZ_JWT_TOKEN as positional arguments, and rotate any exposed keys.

Risk: Delete and unpin operations can remove API keys or pinned content.

Mitigation: Require explicit confirmation and verify target key IDs or pin IDs before running delete_api_key.sh or unpin_file.sh.

Risk: Credential-bearing API calls may follow redirects.

Mitigation: Review endpoint behavior before execution and avoid following redirects with custom credential headers unless the destination is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/namle-aioz/skills/aioz-pin-toolkit)
- [Publisher profile](https://clawhub.ai/user/namle-aioz)
- [AIOZ Pin Documentation](https://docs.pin.aioz.io/)
- [AIOZ Pin MCP Server - API Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, PINNING_API_KEY, and PINNING_SECRET_KEY; AIOZ_JWT_TOKEN is optional for API key management.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
