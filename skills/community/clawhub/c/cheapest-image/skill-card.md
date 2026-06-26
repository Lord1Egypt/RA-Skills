## Description: <br>
Possibly the cheapest AI image generation (~$0.0036/image). Text-to-image via the EvoLink API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pharmacist9527](https://clawhub.ai/user/Pharmacist9527) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to generate images from text prompts through EvoLink z-image-turbo. Agents can run the Python script or documented shell fallbacks, then attach the saved local image file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to EvoLink and may include sensitive content if the user supplies it. <br>
Mitigation: Do not include secrets, personal data, or confidential material in image prompts. <br>
Risk: The EvoLink API key may consume paid credits when image generation requests are submitted. <br>
Mitigation: Use the skill only with an EvoLink key whose spending and access are acceptable for the environment. <br>
Risk: The curl fallback can mishandle prompts that contain quotes or control characters if they are not JSON-escaped. <br>
Mitigation: Prefer the Python script or PowerShell fallback, or JSON-escape prompt text before using the curl heredoc example. <br>


## Reference(s): <br>
- [EvoLink](https://evolink.ai) <br>
- [ClawHub Skill Page](https://clawhub.ai/Pharmacist9527/cheapest-image) <br>
- [PowerShell fallback](artifact/references/powershell.md) <br>
- [curl + heredoc fallback](artifact/references/curl_heredoc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance, image files] <br>
**Output Format:** [Markdown guidance with command examples; scripts print MEDIA:<path> for the generated local image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVOLINK_API_KEY; supports prompt, size, optional seed, NSFW check, output path, and polling controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
