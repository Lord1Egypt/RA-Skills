## Description: <br>
Reads a Markdown file, generates header and section PNG images with the configured OpenClaw image tool, and writes a separate *_img.md copy with images stored in a sibling img folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j3ffyang](https://clawhub.ai/user/j3ffyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and documentation maintainers use this skill to enrich an existing Markdown post or document with generated header and section images while preserving the original file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on locally configured image-provider credentials to generate images. <br>
Mitigation: Keep credentials in environment or config storage, do not paste secrets into chat, and review any generated command before it reads credential files. <br>
Risk: The skill creates files next to the requested Markdown document. <br>
Mitigation: Confirm the input path before running the skill and review the generated *_img.md file and img/ assets before publishing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j3ffyang/blog-image-enricher) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Images, Guidance] <br>
**Output Format:** [Markdown document copy with embedded PNG image references and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a sibling *_img.md file and img/ PNG assets; the original Markdown file remains unchanged.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
