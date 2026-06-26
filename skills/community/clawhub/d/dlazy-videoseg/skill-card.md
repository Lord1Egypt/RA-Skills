## Description: <br>
Segments humans in videos using Aliyun's asynchronous SegmentVideoBody service and returns a same-length black-and-white mask video for compositing or matting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative-production agents use this skill to generate human segmentation masks from input videos for downstream compositing, matting, and video-editing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a dLazy API key, which is sensitive credential material. <br>
Mitigation: Use a scoped organization key where possible, store it only through the documented CLI or environment variable path, and rotate or revoke it from the dLazy dashboard if exposure is suspected. <br>
Risk: Input video files may be uploaded to dLazy-hosted services for processing. <br>
Mitigation: Avoid submitting confidential or regulated media unless the applicable service terms and data-handling requirements have been reviewed. <br>
Risk: The workflow depends on an external npm/npx CLI package and hosted API endpoints. <br>
Mitigation: Review the package and install command before use, pin the documented version, and expect failures when network access, account authorization, or account credits are unavailable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-videoseg) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dLazy API key; successful calls return hosted output URLs or asynchronous task identifiers.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
