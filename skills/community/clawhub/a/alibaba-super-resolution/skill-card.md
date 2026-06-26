## Description: <br>
Enhance video resolution using Alibaba Cloud Super Resolution API. Use when the user wants to: (1) upscale low-res videos to higher resolution, (2) improve video quality before publishing, or (3) convert 480p videos to 1080p. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BlackEight4752](https://clawhub.ai/user/BlackEight4752) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media operators use this skill to upscale low-resolution videos through Alibaba Cloud's Super Resolution API and manage video submission, status checks, and downloads from a CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos are sent to Alibaba Cloud for processing. <br>
Mitigation: Use the skill only for videos authorized for third-party cloud processing, and avoid sensitive media unless policy allows it. <br>
Risk: The skill uses Alibaba Cloud access keys to call the video enhancement API. <br>
Mitigation: Use least-privilege credentials, keep keys in environment variables or a secret manager, and rotate them according to organizational policy. <br>
Risk: Dependency versions are not fully pinned in requirements.txt. <br>
Mitigation: Pin and review dependency versions in controlled environments before deployment. <br>
Risk: Direct uploads are limited to 2GB and output URLs expire after 24 hours. <br>
Mitigation: Use OSS URLs for larger files and download completed outputs promptly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BlackEight4752/alibaba-super-resolution) <br>
- [Alibaba Cloud Super Resolution API documentation](https://help.aliyun.com/zh/viapi/developer-reference/api-w2n4j6) <br>
- [Alibaba Cloud AccessKey documentation](https://help.aliyun.com/zh/viapi/getting-started/create-the-accesskey) <br>
- [Alibaba Cloud SDK documentation](https://help.aliyun.com/document_detail/378659.html) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [CLI output, JSON status objects, and processed video files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Alibaba Cloud credentials for real API calls; demo mode copies the input video when credentials are absent.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
