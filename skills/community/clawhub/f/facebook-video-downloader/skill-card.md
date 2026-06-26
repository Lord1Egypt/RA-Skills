## Description: <br>
Download Facebook videos, Reels, and Stories in HD quality when a user provides a Facebook video URL, with support for HD, SD, and MP3 audio extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankchen622](https://clawhub.ai/user/frankchen622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to fetch downloadable video or audio links for public Facebook videos, Reels, Stories, timeline posts, page videos, and public group videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided Facebook URLs are sent to savefbs.com, including any identifiers or tracking parameters in the URL. <br>
Mitigation: Use only public, non-sensitive Facebook links and remove unnecessary tracking parameters before running the skill. <br>
Risk: The artifact privacy notice claims no user data is transmitted, which conflicts with the security evidence. <br>
Mitigation: Correct the privacy notice and inform users that the third-party service receives the submitted URL. <br>
Risk: The downloader depends on a third-party service whose API behavior or access policy can change. <br>
Mitigation: Review results before sharing links and handle network, HTML, and invalid-response errors as expected failure modes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankchen622/facebook-video-downloader) <br>
- [savefbs.com service](https://savefbs.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON with downloadable media options and concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success or error status, title, thumbnail, and download options with quality, URL, extension, and size when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
