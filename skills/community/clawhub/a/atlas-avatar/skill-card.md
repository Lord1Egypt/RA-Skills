## Description:

Create realtime passthrough AI avatar sessions, view-only viewer tokens, and offline lip-sync avatar videos using the Atlas API by North Model Labs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric-prog](https://clawhub.ai/user/eric-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create and manage Atlas realtime avatar sessions, generate viewer tokens, run offline lip-sync video jobs, and prepare local viewer configuration. It is intended for workflows where the user supplies speech, LLM, or TTS components and Atlas renders the avatar output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow can clone or update external repositories and run npm install while API secrets are available.

Mitigation: Use dedicated low-privilege API keys, inspect or pin external repositories before setup, and avoid pointing ATLAS_AGENT_REPO or ATLAS_REALTIME_EXAMPLE_GIT at untrusted paths or URLs.

Risk: Atlas and optional LLM or ElevenLabs credentials may be written to a local .env.local file.

Mitigation: Keep the viewer checkout private, restrict file permissions, remove local secret files after use, and avoid optional secrets unless the workflow requires them.

Risk: Realtime viewer tokens and presigned result URLs can expose session access or generated media if shared broadly.

Mitigation: Mint viewer tokens only for intended viewers, avoid posting raw tokens in public channels, and treat generated result URLs as sensitive until they expire.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/eric-prog/skills/atlas-avatar)
- [Atlas API reference](references/api-reference.md)
- [North Model Labs API docs](https://www.northmodellabs.com/api)
- [North Model Labs hosted examples](https://www.northmodellabs.com/examples)
- [Atlas realtime example app](https://github.com/NorthModelLabs/atlas-realtime-example)
- [Atlas React package](https://www.npmjs.com/package/@northmodellabs/atlas-react)
- [LiveKit client package](https://www.npmjs.com/package/livekit-client)
- [North Model Labs dashboard](https://dashboard.northmodellabs.com/dashboard/keys)
- [OpenClaw install docs](https://docs.openclaw.ai/install)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands, Python CLI usage, curl examples, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ATLAS_API_KEY and optional Atlas, LLM, and ElevenLabs environment variables depending on the workflow.]

## Skill Version(s):

1.0.9 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
