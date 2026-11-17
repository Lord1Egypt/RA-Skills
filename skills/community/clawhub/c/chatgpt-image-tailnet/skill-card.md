## Description:

Generate and download ChatGPT images through the remote Camoufox browser reachable over the tailnet, especially when residential/IP reputation matters more than the local host IP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lotfinity](https://clawhub.ai/user/lotfinity)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate ChatGPT images through a trusted remote Camoufox browser on a tailnet and capture the resulting image download from the browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a remote browser session through a tailnet HTTP API without clear endpoint-level safeguards.

Mitigation: Install only where you own and trust the browser host and restrict access to port 9377 with tailnet ACLs or firewall rules.

Risk: Prompts and generated images pass through the remote browser session and may be saved to disk.

Mitigation: Avoid sensitive prompts unless endpoint authentication and session isolation are added; review saved files and retention paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lotfinity/skills/chatgpt-image-tailnet)
- [ChatGPT](https://chatgpt.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples; the helper script emits JSON status and saves image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated PNG files to disk via remote browser downloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
