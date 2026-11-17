## Description:

Integrate ClawHub with BlueColumn AI for audio ingest, memory, and semantic retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect ClawHub audio workflows to BlueColumn's ingest, streaming, memory, and semantic retrieval APIs for calls, music, podcasts, voice notes, and live conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to send audio, user references, transcripts, embeddings, and derived analysis to an external BlueColumn service.

Mitigation: Confirm consent, retention, deletion, and access controls before use; minimize enabled processing options and avoid sending unnecessary sensitive data.

Risk: The artifact permits storing a BlueColumn API key in a project document, which can expose credentials.

Mitigation: Use a managed secret store for API keys and do not place credentials in TOOLS.md or other project documents.

## Reference(s):

- [BlueColumn ClawHub Integration on ClawHub](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/bluecolumn-clawhub-integration)
- [BlueColumn audio ingest endpoint](https://api.bluecolumn.ai/v1/audio/ingest)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON request examples and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint paths, WebSocket endpoint guidance, required metadata fields, configuration options, and API key handling guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
