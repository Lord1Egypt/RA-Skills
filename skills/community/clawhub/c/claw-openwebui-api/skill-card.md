## Description:

Integrates OpenClaw with Open WebUI APIs so an agent can chat with models, upload and list files, and search or populate RAG knowledge bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dolphins1123](https://clawhub.ai/user/dolphins1123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to automate authenticated Open WebUI operations, including model discovery, file upload, file listing, chat, and RAG knowledge-base search or ingestion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can transmit prompts, files, and API tokens to an Open WebUI endpoint, including over plaintext HTTP if configured that way.

Mitigation: Use only trusted HTTPS Open WebUI endpoints, avoid the shell helper's default LAN URL, and use a least-privilege API token.

Risk: Uploaded documents may be retained or exposed according to the target Open WebUI server's controls.

Mitigation: Do not upload sensitive documents unless the server's retention, access, and deletion controls are understood and acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dolphins1123/skills/claw-openwebui-api)
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Open WebUI API Endpoint Reference](https://docs.openwebui.com/reference/api-endpoints/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text, JSON API responses, and shell or Python command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENWEBUI_URL and OPENWEBUI_API_KEY; can transmit prompts, API tokens, and uploaded files to the configured Open WebUI endpoint.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
