## Description:

Guide users to configure local Chanjing credentials safely via local commands only, and validate local token status when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binkes](https://clawhub.ai/user/binkes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up, check, and refresh local Chanjing AK/SK and access-token credentials without pasting secrets into chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence marks this release suspicious because Chanjing AK/SK values and access tokens are stored locally and can be exposed if the local environment is mishandled.

Mitigation: Install only if the publisher is trusted, keep the credentials file on a trusted device with restricted permissions, and rotate keys if secrets are exposed.

Risk: The helper can use CHANJING_OPENAPI_BASE_URL or CHANJING_API_BASE to choose the token endpoint.

Mitigation: Set those variables only to trusted Chanjing-compatible endpoints, and leave them unset for the documented default endpoint unless a trusted override is required.

Risk: The token helper may print an access token to stdout.

Mitigation: Treat printed tokens as sensitive material and avoid capturing them in shell history, CI logs, chat transcripts, or shared terminal recordings.

## Reference(s):

- [Credentials Guard Reference](reference.md)
- [Chanjing Documentation](https://doc.chanjing.cc)
- [ClawHub Skill Page](https://clawhub.ai/binkes/skills/chanjing-credentials-guard)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and local credential status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local credential file paths, environment variables, and access-token status.]

## Skill Version(s):

1.0.7 (source: server release evidence; artifact manifest lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
