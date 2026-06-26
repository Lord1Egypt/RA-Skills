## Description: <br>
Generates and edits images through APIYI's GPT Image 2 service, supporting text-to-image, image editing, multi-image fusion, size and quality controls, and local PNG, JPEG, or WebP output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to turn natural-language image requests into CLI calls that create new images, edit existing images, or combine up to five reference images through APIYI. It is useful when an agent needs to preserve the user's prompt, choose output parameters, run the bundled Node.js or Python script, and report the saved image path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference images, and authenticated requests are sent to APIYI for third-party processing. <br>
Mitigation: Use only with content suitable for APIYI processing, and avoid confidential or personal images unless that processing is acceptable. <br>
Risk: API keys may be exposed if passed directly on the command line. <br>
Mitigation: Prefer the APIYI_API_KEY environment variable and avoid sharing command history or logs containing credentials. <br>
Risk: Generated images are written to local files and may overwrite or reveal user-chosen paths if handled carelessly. <br>
Mitigation: Review output filenames and directories before execution, and keep generated files in an appropriate workspace location. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wuchubuzai2018/apiyi-gpt-image-2-gen) <br>
- [APIYI platform](https://api.apiyi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with CLI commands; generated image files are saved locally as PNG, JPEG, or WebP.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIYI_API_KEY or a command-line API key; supports prompt, filename, size, quality, output format, compression, and up to five input images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
