## Description:

Create, configure, and manage UNITH digital human avatars via the UNITH API across video, conversational, document Q&A, Voiceflow, plugin, and embedding workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polucas](https://clawhub.ai/user/polucas)

### License/Terms of Use:


## Use Case:

Developers and builders use this skill to create hosted UNITH digital humans, select faces and voices, configure operating modes, upload knowledge documents, and embed avatars in applications or websites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-bearing UNITH API calls can be redirected if API_BASE is overridden.

Mitigation: Unset or lock down API_BASE before authentication or account actions, and verify that requests target https://platform-api.unith.ai.

Risk: Cached UNITH bearer tokens may expose access to the user's account if stored in a shared or weakly protected location.

Mitigation: Disable UNITH_TOKEN_CACHE or set it to a private user-owned path, keep permissions restrictive, and clear cached tokens after use.

Risk: Secrets or sensitive document details could appear in logged payloads, command-line fields, or shared transcripts.

Mitigation: Keep secrets in environment variables, avoid embedding credentials in payload files or command arguments, and review payloads before sharing logs.

Risk: Deleting a digital human is irreversible.

Mitigation: Require an explicit user confirmation that names the exact digital human before running deletion, then use the script confirmation flag only after that approval.

Risk: The skill can manage hosted avatars and uploaded knowledge documents in the user's UNITH account.

Mitigation: Review planned account actions before execution and limit uploaded documents to content approved for the intended avatar.

## Reference(s):

- [Digital Clawatar on ClawHub](https://clawhub.ai/polucas/skills/digital-clawatar)
- [UNITH API Overview](https://docs.unith.ai/_lgI-overview)
- [UNITH Documentation](https://docs.unith.ai)
- [API Payloads Reference](references/api-payloads.md)
- [Configuration Reference](references/configuration.md)
- [Embedding Reference](references/embedding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON payloads, configuration values, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include hosted avatar URLs, embedding snippets, and instructions for local script execution.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
