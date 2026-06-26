## Description: <br>
Downloads Douyin videos or image galleries from share text, short links, or Douyin page URLs, saving videos as MP4 files and galleries as image folders with optional ZIP packaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[railgun9983](https://clawhub.ai/user/railgun9983) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local Python downloader for Douyin content they are authorized to access, including single videos and image-gallery posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Adding logged-in browser cookies to the script can expose account credentials. <br>
Mitigation: Avoid adding cookies when possible; if required, treat them like passwords, keep them out of source control and shared logs, and remove them immediately after use. <br>
Risk: The downloader can save Douyin media outside the platform. <br>
Mitigation: Use it only for content the user is allowed to access and save, and avoid bulk collection, commercial redistribution, or creator-rights violations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; downloaded media files are MP4, JPG, and optional ZIP archives.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.9+, requests, and network access to Douyin or iesdouyin endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
