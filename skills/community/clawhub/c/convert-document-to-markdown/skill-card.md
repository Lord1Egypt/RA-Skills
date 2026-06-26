## Description: <br>
Convert supported local files into Markdown by running this repository's Dockerized file-only CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kadbbz](https://clawhub.ai/user/kadbbz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert supported local documents, images, and text files into Markdown for downstream processing. It is intended for file-based conversion through a Docker wrapper that returns Markdown, logs, and metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a prebuilt Aliyun Docker image against local document folders. <br>
Mitigation: Use it only when the image source is trusted, keep the mounted input folder limited to the target file, and review scan results before deployment. <br>
Risk: Vision modes can pass VL API credentials and document content to a configured external provider. <br>
Mitigation: Use scoped API keys, keep .env limited to VL settings, and prefer ocr or none mode when external processing is not approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kadbbz/convert-document-to-markdown) <br>
- [ClawHub homepage](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Structured JSON by default, with converted Markdown in the markdown field and optional raw Markdown output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes logs and metadata when JSON output is used; requires Docker and VL configuration for vision modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
