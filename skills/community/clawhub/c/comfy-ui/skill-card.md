## Description:

Generate high-quality images through a user-configured local ComfyUI server with optional custom workflow JSON files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dihan](https://clawhub.ai/user/dihan)

### License/Terms of Use:


## Use Case:

External users, developers, and creative operators use this skill to send prompts and optional workflow JSON to their own ComfyUI server and retrieve locally saved image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A server-controlled filename can cause local files to be written outside the intended image folder.

Mitigation: Use only trusted local ComfyUI servers and harden downloads by sanitizing filenames and verifying that resolved output paths stay inside image-gens/.

Risk: Prompts and workflow content are sent to the configured ComfyUI server.

Mitigation: Use non-sensitive prompts and workflows, and document the configured server before running generation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dihan/skills/comfy-ui)
- [Publisher profile](https://clawhub.ai/user/dihan)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and script output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved locally under image-gens/ by the helper script.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
