## Description:

Generate images using the internal Google Antigravity API (Gemini 3 Pro Image). High quality, native generation without browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ipedrax](https://clawhub.ai/user/ipedrax)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate image files from text prompts through a local Node.js script that uses a configured Google Antigravity OAuth profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local Google Antigravity OAuth profile and sends image prompts to an internal Google sandbox endpoint.

Mitigation: Install only where this credential access and prompt sharing are acceptable, and prefer a documented API with an explicit project and least-privilege credential.

Risk: The skill may consume account or project quota under spoofed client metadata.

Mitigation: Use a dedicated limited project or credential, monitor quota usage, and confirm the API and client metadata are appropriate before use.

Risk: The internal API or model response structure may change and cause generation failures.

Mitigation: Validate generated outputs and review model or API error messages before relying on the produced image file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ipedrax/skills/antigravity-image-gen)
- [Publisher profile](https://clawhub.ai/user/ipedrax)
- [ClawHub registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [PNG image file path with console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and a configured auth.profiles entry; prints MEDIA: <path> when an image is saved.]

## Skill Version(s):

2.0.0 (source: server release metadata and target metadata; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
