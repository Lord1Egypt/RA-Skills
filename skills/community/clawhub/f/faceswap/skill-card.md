## Description: <br>
AI Face Swap - Swap face in video using verging.ai API. Supports local video files, YouTube/Bilibili URLs, local and remote face images. Auto-download, trimming, real-time progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[revisual-ai](https://clawhub.ai/user/revisual-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run command-line face swaps on video using the verging.ai API with local files, supported video URLs, and local or remote face images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends face images and video media to a third-party service for processing. <br>
Mitigation: Use only media where consent and rights are documented, and avoid private, regulated, intimate, or non-consensual content unless the publisher documents privacy, retention, deletion, and acceptable-use controls. <br>
Risk: The skill requires a sensitive verging.ai API key. <br>
Mitigation: Store the key in VERGING_API_KEY or pass it only at runtime, never commit it to public repositories, and rotate it if exposure is suspected. <br>
Risk: Temporary media files are written under /tmp/verging-faceswap/ during processing. <br>
Mitigation: Remove temporary files after use and avoid shared systems for sensitive media unless local access controls are appropriate. <br>


## Reference(s): <br>
- [ClawHub Faceswap release](https://clawhub.ai/revisual-ai/faceswap) <br>
- [Publisher profile](https://clawhub.ai/user/revisual-ai) <br>
- [verging.ai](https://verging.ai) <br>
- [verging.ai API docs](https://verging.ai/docs/api) <br>
- [Face Swap demo](https://youtu.be/xvlZe4uqvY4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return verging.ai job status, result URLs, and optional downloaded video files.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
