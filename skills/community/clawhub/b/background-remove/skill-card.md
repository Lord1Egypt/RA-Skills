## Description: <br>
Removes backgrounds from JPG, PNG, or WebP images by sending a selected local file or downloaded URL image to the verging.ai background-removal API and returning a transparent PNG result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alouhaou](https://clawhub.ai/user/alouhaou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content automation agents use this skill to remove image backgrounds through verging.ai and optionally save the transparent PNG output locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to verging.ai for background-removal processing. <br>
Mitigation: Use only images appropriate for third-party processing, and avoid private, internal, signed, or sensitive image URLs unless verging.ai data handling and retention terms have been reviewed. <br>
Risk: The skill requires a VERGING_API_KEY credential. <br>
Mitigation: Store the key in the environment or a secrets manager, avoid committing it to repositories, and review generated commands before sharing logs or transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alouhaou/background-remove) <br>
- [verging.ai website](https://verging.ai) <br>
- [verging.ai API docs](https://verging.ai/docs/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline curl commands, API result URLs, and optional local PNG download instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and VERGING_API_KEY. Supports JPG, PNG, and WebP inputs up to 10 MB and consumes one verging.ai credit per image.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
