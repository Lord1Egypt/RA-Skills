## Description:

Guides agents through creating and extending Luma Dream Machine videos through AceDataCloud's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to prepare text-to-video, image-to-video, and video-extension requests and follow up on generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video prompts, public reference image URLs, and task data are sent to AceDataCloud.

Mitigation: Share only data you are comfortable sending under your account and avoid sensitive reference images.

Risk: The AceDataCloud API key may be exposed in prompts or committed files.

Mitigation: Keep the key out of prompts and repositories, store it in an environment file, and use a restricted key where available.

Risk: Resubmitting an asynchronous generation request to check progress may incur another charge.

Mitigation: Poll the existing task ID rather than submitting the same request again.

Risk: The optional mcp-luma package adds third-party software to the environment.

Mitigation: Verify the package before installing it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/acedatacloud/skills/luma)
- [AceDataCloud key setup and first run](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud asynchronous task guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)
- [AceDataCloud MCP server guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/mcp-servers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides API requests and task polling; generated videos are returned by the external service, not by this skill.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
