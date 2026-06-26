## Description: <br>
Convert any URL or file to Markdown. Supports webpage, WeChat, YouTube, Bilibili, Douyin, Xiaohongshu, PDF, and Office files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haiwenai](https://clawhub.ai/user/haiwenai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to convert webpages, social/video links, and local documents into Markdown for notes, documentation, or downstream agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube conversions may retry with Chrome browser cookies, which can expose a logged-in browser context. <br>
Mitigation: Use a dedicated browser profile or require explicit approval before cookie-based retry, prefer stdout output, and avoid sensitive paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haiwenai/anything-to-md) <br>
- [Project homepage](https://github.com/haiwenai/anything-to-md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands] <br>
**Output Format:** [Markdown with YAML frontmatter; video conversions may include a timestamped transcript section.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses stdout by default and can save output to a file or directory when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
