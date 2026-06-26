## Description: <br>
Generates Studio Ghibli style AI images through the Neta AI image generation API and returns a direct image URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wkl-nieta](https://clawhub.ai/user/wkl-nieta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate stylized AI images from text prompts, with optional size and reference-image parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image IDs, and API credentials are sent to the disclosed Neta/TalesOfAI service. <br>
Mitigation: Avoid confidential or personal content, verify trust in the service before use, and use a limited-scope API token that can be revoked. <br>
Risk: The skill depends on an external image-generation service, so availability, moderation, and output quality are outside the local agent's control. <br>
Mitigation: Review generated image URLs and outputs before relying on them, and handle service errors or timeouts in downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wkl-nieta/ghibli-style-skill) <br>
- [Neta API access](https://www.neta.art/open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL printed to stdout, with setup and command guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; prompts and reference image IDs are sent to the Neta/TalesOfAI service.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
