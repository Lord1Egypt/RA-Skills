## Description:

Generate ai blog image generator images with AI via the Neta AI image generation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[barbaraledbettergq](https://clawhub.ai/user/barbaraledbettergq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to generate blog hero or inline images from text prompts through the Neta AI image generation API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generation requests are sent to the external Neta/talesofai.com service.

Mitigation: Use only prompts and reference IDs that are acceptable to share with that service.

Risk: The Neta token may be exposed when passed on the command line or recorded in process listings or logs.

Mitigation: Prefer a limited-scope or disposable Neta token, and avoid logging commands that include --token values.

Risk: The skill depends on an external image-generation service and returns externally hosted image URLs.

Mitigation: Review generated images and handle timeout, moderation, or failed-result cases before publishing or embedding outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/barbaraledbettergq/skills/blog-image-claw-skill)
- [Neta AI API access](https://www.neta.art/open/)
- [Neta API service endpoint](https://api.talesofai.com)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Plain text image URL or JSON status object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Neta API token; generation polls for completion and returns an externally hosted image URL when successful.]

## Skill Version(s):

2.0.1 (source: evidence.release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
