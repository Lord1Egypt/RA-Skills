## Description: <br>
Remove visible Gemini AI watermarks from images via reverse alpha blending. Use for cleaning Gemini-generated images, removing the star/sparkle logo watermark. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[FZLRA](https://clawhub.ai/user/FZLRA) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and image workflow users use this skill to run a local Python utility that removes visible bottom-right Gemini watermark logos from images they are authorized to edit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can remove visible AI provenance watermarks before sharing or publishing images. <br>
Mitigation: Use it only on images you are authorized to edit, and do not use it to hide AI origin, bypass platform rules, or misrepresent generated media. <br>
Risk: Running third-party image-processing code can alter source assets or introduce local execution risk. <br>
Mitigation: Review the skill before installing, run it in a virtual environment, and keep original image files unchanged. <br>
Risk: Edited images may still need AI-origin disclosure even after visible watermark cleanup. <br>
Mitigation: Preserve appropriate AI-origin disclosure when sharing edited images. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FZLRA/gemini-watermark-remover) <br>
- [README.md](artifact/README.md) <br>
- [README_zh.md](artifact/README_zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local command guidance for generating edited image files; no remote image upload is described.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
