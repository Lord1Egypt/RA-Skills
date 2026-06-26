## Description: <br>
Fetches WeChat public-account articles from mp.weixin.qq.com links and saves them as local HTML with downloaded article images and video cover images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aga-j](https://clawhub.ai/user/aga-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to archive WeChat public-account articles for local offline viewing, including article text, images, and video cover references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script can automatically start a background HTTP server from the OpenClaw workspace, which may expose files beyond the saved article. <br>
Mitigation: Run it only in a clean workspace, stop the server after use, and prefer a version that serves only a dedicated output directory on localhost. <br>
Risk: The skill fetches and saves third-party article content and media from WeChat links. <br>
Mitigation: Use it only for content you are permitted to access and archive, and review saved output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aga-j/aga-wechat-article-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Console status text plus local HTML and downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated article HTML, images, and video cover files under the OpenClaw workspace and reports a local preview URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
