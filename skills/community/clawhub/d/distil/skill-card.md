## Description:

Fetch web pages as clean Markdown and search the web via the distil.net proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikel](https://clawhub.ai/user/mikel)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to fetch web pages, search results, rendered pages, raw page content, and screenshots through the Distil proxy for research and documentation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs, query strings, screenshots, and fetched content are sent through a configured Distil proxy endpoint.

Mitigation: Use only trusted HTTPS proxy endpoints and avoid sending secrets, private internal URLs, sensitive query strings, or regulated data unless the proxy is approved for that use.

Risk: Screenshot output can write page images to local paths and may retain sensitive visual content.

Mitigation: Choose screenshot output paths deliberately and remove sensitive images when they are no longer needed.

Risk: Changing DISTIL_PROXY_URL can redirect traffic and API-key use to a different endpoint.

Mitigation: Keep DISTIL_PROXY_URL pinned to a trusted HTTPS endpoint.

## Reference(s):

- [Distil](https://distil.net)
- [Distil Skill on ClawHub](https://clawhub.ai/mikel/skills/distil)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown, raw text, image files, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DISTIL_API_KEY and optional DISTIL_PROXY_URL; HTTP errors return non-2xx status with an error payload.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
