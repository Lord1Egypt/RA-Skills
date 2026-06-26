## Description: <br>
Generates PNG images from text prompts using Baidu's ERNIE-Image API and supported preset resolutions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[livingbody](https://clawhub.ai/user/livingbody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to request a Baidu ERNIE-Image text-to-image generation, choose an output resolution, and save the generated PNG in the current workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation requests are sent to Baidu for processing. <br>
Mitigation: Use this skill only for prompts that are appropriate to share with Baidu AI Studio. <br>
Risk: The artifact documentation advertises image editing and --input-image support, but the authoritative security summary says to treat this release as text-to-image only. <br>
Mitigation: Do not rely on image-editing behavior for this version; use only text prompts, output filenames, and supported resolutions. <br>
Risk: API keys can be exposed when passed in chat or command-line arguments. <br>
Mitigation: Prefer an environment variable such as ERNIE_Image_API_KEY or BAIDU_API_KEY instead of passing the key directly. <br>
Risk: Generated output may overwrite an existing file at the requested path. <br>
Mitigation: Choose explicit, unique output filenames before running the generation script. <br>


## Reference(s): <br>
- [Baidu AI Studio access token](https://aistudio.baidu.com/account/accessToken) <br>
- [Baidu AI Studio ERNIE-Image](https://aistudio.baidu.com/ernieimage) <br>
- [Baidu AI Studio ERNIE-Image model details](https://aistudio.baidu.com/modelsdetail/46030/intro) <br>
- [Baidu AI Studio ERNIE-Image blog](https://aistudio.baidu.com/blog/detail/794723628346373) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PNG file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one image per script invocation; supported resolutions are 1024x1024, 1376x768, 1264x848, 1200x896, 896x1200, 848x1264, and 768x1376.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
