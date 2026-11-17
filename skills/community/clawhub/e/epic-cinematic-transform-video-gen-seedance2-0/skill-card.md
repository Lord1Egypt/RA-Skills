## Description:

Transforms text briefs or public HTTPS image URLs into epic cinematic WeryAI Seedance 2.0 video generations with expanded production prompts and playable Markdown links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to turn ordinary text briefs or public image URLs into trailer-style short videos. It guides prompt expansion, request confirmation, and Seedance 2.0 video generation through WeryAI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid generation can spend WeryAI credits, especially on repeated wait runs.

Mitigation: Show and confirm the full request, including duration, resolution, audio, and model, before submitting or rerunning generation.

Risk: Prompts and public image URLs are sent to WeryAI.

Mitigation: Avoid secrets or private content in prompts, and use only intentional public HTTPS image URLs.

Risk: The bundled CLI can perform broader WeryAI video actions than the advertised Seedance 2.0-only workflow.

Mitigation: Validate every request uses SEEDANCE_2_0 and only supported fields before execution.

Risk: The WERYAI_API_KEY is a required secret.

Mitigation: Provide it only through the runtime environment, do not commit it, and prefer short-lived or isolated execution environments for higher assurance.

## Reference(s):

- [WeryAI Video API Reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/epic-cinematic-transform-video-gen-seedance2-0)
- [Publisher Profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with confirmation tables, inline video links, and JSON CLI request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, public HTTPS image URLs for image-to-video, and the SEEDANCE_2_0 model.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
