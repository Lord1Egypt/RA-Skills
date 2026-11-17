## Description:

Generates 360-degree panoramas with Insta360 DiT360, converts outputs to JPG, and creates an interactive viewer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate AI-based 360-degree panorama images from text prompts, convert the generated image to JPG, and open it in a local interactive Pannellum viewer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill automatically installs an unpinned Python dependency.

Mitigation: Review or modify the skill before deployment to pin dependencies and run it in an isolated virtual environment.

Risk: The release evidence reports that the skill sends prompts to Hugging Face.

Mitigation: Avoid entering sensitive prompts unless the intended Hugging Face Space and data handling are acceptable for the use case.

Risk: The release evidence reports that the skill starts a background local file server with broader network exposure than users are told.

Mitigation: Bind the server to 127.0.0.1, add a clear shutdown path, and review local network exposure before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hongjiahao371-pixel/skills/dit360-panorama-generator)
- [DiT360 GitHub Repository](https://github.com/Insta360-Research-Team/DiT360)
- [DiT360 Hugging Face Space](https://huggingface.co/spaces/Insta360-Research/DiT360)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Generated WebP and JPG image files, an HTML viewer file, local viewer URL, and command-line status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The artifact describes 2048x1024 panorama images, prompt/seed/step parameters, and a local viewer served on port 8899.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
