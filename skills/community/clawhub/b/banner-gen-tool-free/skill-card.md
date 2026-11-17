## Description:

Helps agents generate or edit banner illustrations through an image-generation API, using 1K, 2K, and 4K resolution choices with a draft-to-final workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create or edit individual banner images with prompt-driven image-generation workflows, resolution selection, and API-key based setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious because it requests execution/write authority and includes broad automation instructions beyond banner generation.

Mitigation: Review before installing, and only allow exec/write use for clearly identified image-generation commands you trust.

Risk: API keys may be exposed if supplied directly in command arguments or copied into files.

Mitigation: Prefer environment variables for API keys and avoid passing secrets on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/banner-gen-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and expected PNG image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses prompt text, optional input image path, output filename, resolution choice, and API key configuration.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
