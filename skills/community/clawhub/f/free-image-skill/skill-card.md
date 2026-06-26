## Description: <br>
Provides a workflow for planning image needs, generating priority images with OpenAI credits, searching free image sources, removing permitted watermarks, and batch-processing image outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[titancheung](https://clawhub.ai/user/titancheung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, developers, and marketing teams can use this skill to assemble image assets for articles, reports, social posts, and similar content workflows while prioritizing free sources and controlled API spending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Watermark removal can violate license terms or creator rights when used on images the user is not authorized to modify. <br>
Mitigation: Only process images you own or are explicitly authorized to modify, and preserve required attribution and license records. <br>
Risk: The skill handles OPENAI_API_KEY and can spend API credits when image generation scripts are executed. <br>
Mitigation: Use environment variables for credentials, avoid sharing keys, set hard billing limits, and run plan-only or dry-run modes before generation. <br>
Risk: Free image source licenses and attribution requirements vary by provider and asset. <br>
Mitigation: Review each selected asset's license and attribution requirements before commercial use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/titancheung/free-image-skill) <br>
- [使用示例](references/使用示例.md) <br>
- [项目说明](references/项目说明.md) <br>
- [Unsplash](https://unsplash.com) <br>
- [Pexels](https://www.pexels.com) <br>
- [Pixabay](https://pixabay.com) <br>
- [Freepik](https://www.freepik.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python scripts, JSON configuration, and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may create image files, optimized WebP outputs, and JSON or Markdown indexes when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
