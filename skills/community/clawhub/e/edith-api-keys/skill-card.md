## Description:

Manage Edith smart glasses API keys with Unkey by creating, revoking, listing, verifying, and updating keys through voice-guided commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samdickson22](https://clawhub.ai/user/samdickson22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Unkey-backed API keys for Edith smart glasses integrations, including creating, listing, verifying, updating, and revoking keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful Unkey root credential can create, update, and delete API keys.

Mitigation: Install only in trusted operator environments, prefer least-privileged Unkey credentials when available, and require explicit confirmation for create, update, and delete actions.

Risk: Shell command templates may expose generated keys or handle JSON input unsafely.

Mitigation: Avoid logging or sharing generated keys and replace shell templates with a structured HTTP client or JSON serializer before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samdickson22/skills/edith-api-keys)
- [Unkey API](https://api.unkey.dev)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses UNKEY_ROOT_KEY and UNKEY_API_ID environment variables; generated API keys may be displayed once.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/shipables.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
