## Description:

Generate images with Flux 2 Klein on RunComfy using model-specific prompting guidance, RunComfy CLI commands, and variant selection guidance for fast concepting or polished image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creative teams, and external users use this skill to generate images through the RunComfy CLI with Flux 2 Klein, choosing the 4B variant for rapid iteration or the 9B variant for final-quality output. It also helps agents produce prompt patterns, JSON inputs, and safe invocation guidance for RunComfy-hosted image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts can be handled unsafely if interpolated directly into shell command examples.

Mitigation: Construct the RunComfy --input payload with a JSON serializer and pass arguments safely instead of raw shell string substitution.

Risk: Global CLI installation can increase supply-chain exposure.

Mitigation: Prefer a pinned, project-local RunComfy CLI installation and keep RUNCOMFY_TOKEN scoped to the generation process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/permew/skills/flux-2-klein)
- [RunComfy](https://www.runcomfy.com)
- [Flux 2 Klein 9B Model](https://www.runcomfy.com/models/blackforestlabs/flux-2-klein/9b/text-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein)
- [Flux 2 Klein 4B Model](https://www.runcomfy.com/models/blackforestlabs/flux-2-klein/4b/text-to-image?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein)
- [RunComfy CLI Introduction](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein)
- [RunComfy CLI Troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=flux-2-klein)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with bash command examples and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce RunComfy CLI result JSON and downloaded image files in the requested output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
