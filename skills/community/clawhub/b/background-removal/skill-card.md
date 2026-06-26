## Description: <br>
Removes backgrounds from images with the BiRefNet model via the inference.sh CLI, producing transparent PNGs for product photos, portraits, marketing, social media, and design. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and image-workflow users use this skill to run inference.sh image applications for removing or changing image backgrounds, especially for product photos, portraits, marketing assets, social media images, and design compositions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The quick-start path fetches and runs a remote CLI installer before background-removal use. <br>
Mitigation: Inspect the inference.sh install script or use the documented manual install and checksum verification path before running it. <br>
Risk: Using the skill can require authenticating with inference.sh and submitting images to that provider for processing. <br>
Mitigation: Run it only when the provider and account context are trusted for the images being processed. <br>


## Reference(s): <br>
- [inference.sh Running Apps](https://inference.sh/docs/apps/running) <br>
- [inference.sh Image Generation Example](https://inference.sh/docs/examples/image-generation) <br>
- [inference.sh Apps Overview](https://inference.sh/docs/apps/overview) <br>
- [inference.sh CLI Checksums](https://dist.inference.sh/cli/checksums.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs inference.sh image applications that return PNG images with transparent backgrounds.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
