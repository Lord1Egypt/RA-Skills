## Description: <br>
Call Cutout.Pro visual processing APIs to perform background removal, face cutout, and photo enhancement with file upload or image URL input, returning binary streams or Base64-encoded results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cutout-pro](https://clawhub.ai/user/cutout-pro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and image-processing agents use this skill to run Cutout.Pro operations for background removal, face and hair cutouts, optional facial landmarks, and photo enhancement from local files or image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local images, image URLs, and optional face landmark data are sent to Cutout.Pro for processing. <br>
Mitigation: Avoid sensitive photos, confidential documents, internal image URLs, or identifiable faces unless the user has permission and accepts third-party processing. <br>
Risk: The skill requires a Cutout.Pro API key and consumes Cutout.Pro credits. <br>
Mitigation: Keep CUTOUT_API_KEY private, do not commit .env files, and use preview mode when appropriate to reduce credit usage. <br>


## Reference(s): <br>
- [Cutout Visual API Skill Page](https://clawhub.ai/cutout-pro/cutout-visual-api) <br>
- [Publisher Profile](https://clawhub.ai/user/cutout-pro) <br>
- [API Reference](references/api-reference.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Cutout.Pro](https://www.cutout.pro) <br>
- [Cutout.Pro API Key](https://www.cutout.pro/user/secret-key) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; the script can produce image files, metadata JSON, Base64 image data, and optional face landmark JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written under data/outputs by default, with optional .meta.json metadata for saved binary image results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and script version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
