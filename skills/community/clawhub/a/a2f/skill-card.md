## Description: <br>
Archive2Figure (a2f) helps agents convert PDF archives containing character information into digital character figure images by extracting features, generating prompts, submitting image-generation jobs, and polling for results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wadipapa](https://clawhub.ai/user/wadipapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to work with the Archive2Figure API for extracting character features from PDFs, creating feature-based prompts, generating character images, and retrieving image result URLs. It is especially oriented toward Chinese historical character and realistic portrait workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected local PDFs, extracted character data, prompts, job IDs, and generated-output requests to wuji.cyphy.com. <br>
Mitigation: Use it only for explicit requests, review the PDF path before upload, and confirm the user is comfortable sending that data to the external service. <br>
Risk: Confidential, regulated, private, or copyrighted PDFs could be exposed if used without proper authorization. <br>
Mitigation: Do not use those materials unless authorization and the service's data handling are understood. <br>


## Reference(s): <br>
- [ClawHub a2f skill page](https://clawhub.ai/wadipapa/a2f) <br>
- [Publisher profile](https://clawhub.ai/user/wadipapa) <br>
- [Wuji API base](https://wuji.cyphy.com/api) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, JSON API payloads, endpoint descriptions, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include instructions for uploading PDFs and prompts to wuji.cyphy.com, polling job IDs, and handling generated image URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
