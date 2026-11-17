## Description:

Generate images, videos, and process media using the GenVR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genvrlabs](https://clawhub.ai/user/genvrlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to list GenVR models, submit image or video generation jobs, poll task status, and retrieve generated media through the GenVR API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI loads environment variables from a local .env file, which may expose unrelated secrets from the current working directory.

Mitigation: Run the skill from a dedicated directory containing only the required GENVR_API_KEY and GENVR_UID values.

Risk: Unpinned npx execution can run a mutable package version.

Mitigation: Use a reviewed, pinned package version for production or sensitive workflows.

Risk: The output filename option can overwrite writable files when pointed at important paths.

Mitigation: Use generated default filenames or restrict --filename to a safe relative path in a scratch output directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/genvrlabs/skills/genvr-skills)
- [GenVR API Access](https://api.genvrresearch.com/obtain-api)
- [GenVR API](https://api.genvrresearch.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with inline shell commands, plus generated media files or JSON status output from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GENVR_API_KEY and GENVR_UID for most operations; generation tasks may run asynchronously.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
