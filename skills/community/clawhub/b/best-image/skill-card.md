## Description: <br>
Best quality AI image generation (~$0.12-0.20/image), including text-to-image, image-to-image, and image editing via the EvoLink API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pharmacist9527](https://clawhub.ai/user/Pharmacist9527) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate, transform, or edit images through EvoLink from prompts and optional reference image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, and the EvoLink API key are sent to EvoLink. <br>
Mitigation: Keep the key in EVOLINK_API_KEY, avoid sensitive prompts or private image URLs, and install only if EvoLink data handling is acceptable. <br>
Risk: Image generation can spend EvoLink API credits, and 4K quality may cost more. <br>
Mitigation: Confirm the requested quality and expected cost before running high-volume or 4K generations. <br>
Risk: A user-selected output path could overwrite an important local file. <br>
Mitigation: Write generated images to a noncritical path and avoid using existing important filenames. <br>


## Reference(s): <br>
- [Best Image on ClawHub](https://clawhub.ai/Pharmacist9527/best-image) <br>
- [EvoLink](https://evolink.ai) <br>
- [curl heredoc fallback](references/curl_heredoc.md) <br>
- [PowerShell fallback](references/powershell.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Local image file path emitted as MEDIA:<path>, with Markdown and shell guidance for fallback workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOLINK_API_KEY; supports size, quality, and up to 10 reference image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
