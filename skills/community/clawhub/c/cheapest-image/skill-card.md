## Description:

Possibly the cheapest AI image generation (~$0.0036/image). Text-to-image via the EvoLink API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pharmacist9527](https://clawhub.ai/user/pharmacist9527)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate low-cost images from text prompts through EvoLink, with Python as the primary path and PowerShell or curl fallbacks when Python is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and the API key are sent to EvoLink.

Mitigation: Use non-sensitive prompts, protect EVOLINK_API_KEY, and review EvoLink terms and data handling before use.

Risk: The skill downloads provider-returned result URLs without explicit destination or size limits.

Mitigation: Run it in a controlled working directory, avoid privileged paths, and monitor downloaded file size and storage use.

## Reference(s):

- [EvoLink](https://evolink.ai)
- [Cheapest Image ClawHub listing](https://clawhub.ai/pharmacist9527/skills/cheapest-image)
- [PowerShell fallback](references/powershell.md)
- [curl + heredoc fallback](references/curl_heredoc.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python, PowerShell, and curl command examples; execution emits MEDIA:<path> for a local generated image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EVOLINK_API_KEY and writes generated image files locally.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
