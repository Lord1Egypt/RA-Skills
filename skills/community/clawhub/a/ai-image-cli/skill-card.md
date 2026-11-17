## Description:

AI image generation tool supporting text-to-image and image-to-image workflows through the AIGW API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxxxxzh1](https://clawhub.ai/user/xxxxxzh1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images from text prompts, edit images from source URLs, inspect tool capabilities, and recover from installation or authentication errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer uses unsafe package-installation and credential-handling patterns, including an internal package index and exposed repository credentials.

Mitigation: Review the installer before use, trust the package index only in controlled environments, prefer HTTPS with pinned hashes, and rotate or remove exposed repository credentials.

Risk: The scripts may source ~/.openclaw/user.env as shell code.

Mitigation: Allow only trusted users and processes to write that file, and inspect its contents before running the install or preflight scripts.

Risk: Prompts, image URLs, and authentication material may be sent to documented remote services.

Mitigation: Avoid submitting sensitive prompts, private image URLs, or secrets unless the deployment accepts those remote-service data flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xxxxxzh1/skills/ai-image-cli)
- [CLI reference](references/cli-reference.md)
- [Usage examples](references/examples.md)

## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image-generation command results include success status, command name, provider data, generated image URLs, usage details, or error hints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
