## Description:

AITuber API skill for AI video creation that helps agents generate videos with AI narration, visuals, captions, MP4 export, and downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhivalogu](https://clawhub.ai/user/dhivalogu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to let supported coding agents call the AITuber API for creating social or long-form videos from scripts or ideas, selecting voices and styles, checking credits, exporting MP4 files, and downloading rendered output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions may run unpinned third-party packages.

Mitigation: Install only from a reviewed, pinned version or use the manual SKILL.md install path.

Risk: Authenticated API calls can consume account credits when generating videos.

Mitigation: Confirm credit-spending actions before generation and check subscription or credit balance when appropriate.

Risk: AITUBER_API_KEY is an account credential.

Mitigation: Store it only in the environment and avoid exposing it in prompts, logs, or generated files.

Risk: The example download command writes to video.mp4 and may overwrite an existing file.

Mitigation: Change the output filename before downloading when video.mp4 already exists.

## Reference(s):

- [AITuber](https://aituber.app)
- [AITuber API Documentation](https://aituber.app/api)
- [AITuber API Docs](https://app.aituber.app/api-docs)
- [AITuber OpenAPI Spec](https://app.aituber.app/api/v1/openapi.json)
- [AITuber MCP Server](https://github.com/aituberapp/aituber-mcp)
- [ClawHub Skill Page](https://clawhub.ai/dhivalogu/skills/ai-video-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with curl command examples and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AITUBER_API_KEY for authenticated endpoints; generated videos may consume account credits; MP4 downloads use temporary signed URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
