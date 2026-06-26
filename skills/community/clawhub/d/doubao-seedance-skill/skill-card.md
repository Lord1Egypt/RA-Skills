## Description: <br>
Calls the Volcengine Seedance video generation API for text-to-video, image-to-video, and first-frame-to-last-frame video generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lamuier](https://clawhub.ai/user/Lamuier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate videos through Volcengine Seedance from text prompts, reference images, or first and last frame inputs. It is useful when an agent should submit a video generation task, poll for completion, and return a local video file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to Volcengine, and API usage may consume quota or incur charges. <br>
Mitigation: Use a Volcengine API key scoped for the intended environment, keep it out of shared files and logs, and review usage before running generation requests. <br>
Risk: The script can download generated video content to a local output directory. <br>
Mitigation: Review the output directory before relying on generated files, and consider adding URL validation, request timeouts, and size limits for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Lamuier/doubao-seedance-skill) <br>
- [Volcengine Seedance task API endpoint](https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOLCENGINE_API_KEY and may save generated MP4 files to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
