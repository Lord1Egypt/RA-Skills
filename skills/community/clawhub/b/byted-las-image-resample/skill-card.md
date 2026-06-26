## Description: <br>
Downsamples, resizes, compresses, converts, and adjusts DPI for JPEG, PNG, and TIFF images through Volcengine LAS, including thumbnail and batch workflows with downscale-only limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Volcengine LAS image-resampling jobs, estimate pricing, upload local images when needed, run lasutil commands, and present output TOS paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Volcengine credentials and may process user images through Volcengine LAS. <br>
Mitigation: Use least-privilege credentials, confirm region and TOS bucket alignment, and avoid sensitive images unless remote processing is acceptable. <br>
Risk: The setup workflow may download and install a remote SDK without a hash or signature verification step. <br>
Mitigation: Review the setup script before use and run it only in environments where installing the remote SDK is acceptable. <br>


## Reference(s): <br>
- [las_image_resample API Reference](references/api.md) <br>
- [Pricing Information](references/prices.md) <br>
- [Volcengine LAS Pricing](https://www.volcengine.com/docs/6492/1544808) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes price-estimation guidance, required credential checks, LAS request configuration, execution commands, and result summaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
