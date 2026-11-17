## Description:

Connect to Fathom AI to fetch call recordings, transcripts, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucassynnott](https://clawhub.ai/user/lucassynnott)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to list Fathom meetings, fetch call transcripts, retrieve summaries and action items, and search meeting records they are authorized to access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The webhook setup can continuously send transcripts, summaries, and action items to a user-supplied HTTPS endpoint.

Mitigation: Run setup-webhook.sh only for an endpoint you control, confirm the destination is intended for meeting content, and delete the webhook when it is no longer needed.

Risk: Fathom call recordings, transcripts, summaries, and action items may contain sensitive meeting content.

Mitigation: Use the read-only scripts only with meetings you are authorized to access and avoid exposing returned content in logs or shared terminals.

Risk: The Fathom API key grants access to meeting data available to that account.

Mitigation: Store the API key securely, prefer a protected environment variable or chmod 600 key file, and rotate the key if it is exposed.

## Reference(s):

- [ClawHub Fathom Skill](https://clawhub.ai/lucassynnott/skills/fathom)
- [Fathom](https://fathom.video)
- [Fathom Developer Portal](https://developers.fathom.ai)
- [Fathom External API Base URL](https://api.fathom.ai/external/v1)
- [Publisher Profile](https://clawhub.ai/user/lucassynnott)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, JSON, and shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a Fathom API key supplied through FATHOM_API_KEY or ~/.fathom_api_key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
