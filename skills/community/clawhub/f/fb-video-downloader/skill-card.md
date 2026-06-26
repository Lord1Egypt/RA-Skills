## Description: <br>
Downloads Facebook videos, Reels, and Stories by calling savefbs.com and returning available download options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankchen622](https://clawhub.ai/user/frankchen622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when they have a Facebook video, Reel, Story, or public post URL and want download links for offline personal access or audio extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Facebook video URLs are sent to savefbs.com, while the security evidence says not to rely on the skill's no-transmission privacy claim. <br>
Mitigation: Install only if sending the target Facebook URLs to savefbs.com is acceptable, avoid private or sensitive content URLs, and review the returned links before use. <br>
Risk: The skill includes a hardcoded crypto payment flow for unlimited downloads. <br>
Mitigation: Do not pay through the displayed crypto payment link unless the publisher provides a verified billing and unlock process. <br>
Risk: The authoritative security verdict is suspicious because the skill likely performs the advertised task but includes misleading privacy claims and payment behavior that requires review. <br>
Mitigation: Use a review-before-execution posture, inspect script behavior before running it, and treat payment and quota messaging as unverified publisher-provided functionality. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankchen622/fb-video-downloader) <br>
- [Publisher profile](https://clawhub.ai/user/frankchen622) <br>
- [savefbs.com](https://savefbs.com) <br>
- [savefbs.com pricing](https://savefbs.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown command guidance and JSON responses containing success status, metadata, download links, quota state, and errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a Python script against savefbs.com, stores a local daily usage counter, and may return payment or upgrade information when the free quota is exhausted.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
