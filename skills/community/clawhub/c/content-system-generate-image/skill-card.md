## Description:

Generate article companion images for the content factory pipeline. Use when Codex needs article images, infographic cards, inline visuals, or a PNG exported from an article markdown draft before preview or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-production teams use this skill to turn article Markdown drafts into companion article images, including header art, infographic cards, and inline visuals. It supports external image generation and a local fallback information-card renderer when the external backend is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article Markdown frontmatter can override the image provider, API base, and model used for credential-bearing image requests.

Mitigation: Use only trusted drafts and trusted image endpoints, or restrict per-article endpoint overrides before running the skill.

Risk: Sensitive draft content may be sent to the configured external image endpoint during generation.

Mitigation: Avoid processing sensitive drafts unless the configured endpoint and credential handling meet the deployment's data-handling requirements.

Risk: External image generation can fail because of network, API, or credential issues.

Mitigation: Rely on the documented local fallback for continuity and review fallback images before preview or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/content-system-generate-image)
- [Suxi image API base](https://new.suxi.ai/v1)
- [Suxi login](https://job.suxi.ai/)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image file with Markdown command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary exported file is content-production/ready/<slug>-img-1.png; fallback output is a valid local information-card PNG.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
