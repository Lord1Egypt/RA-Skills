## Description: <br>
Downloads the latest TikTok video, multiple recent videos, or metadata from a public TikTok profile or direct video URL using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stoxca](https://clawhub.ai/user/stoxca) <br>

### License/Terms of Use: <br>
OpenClaw Knowledge Base License (KBLICENSE) <br>


## Use Case: <br>
External users and developers use this skill to retrieve authorized TikTok media or metadata from public profiles or direct video URLs while managing output paths and common yt-dlp errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update yt-dlp with pip and --break-system-packages when yt-dlp is missing. <br>
Mitigation: Install and pin dependencies in a controlled environment before enabling the skill; avoid allowing the agent to modify system Python packages during normal use. <br>
Risk: Cookie workflows can expose authenticated TikTok account access. <br>
Mitigation: Use browser or exported cookies only with explicit approval in a controlled session, and avoid sharing cookie files. <br>
Risk: Downloading or archiving third-party TikTok content can violate rights, privacy expectations, or platform terms. <br>
Mitigation: Use it only for content the user owns, has permission to download, or may lawfully archive; review applicable terms before bulk downloads. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stoxca/download-video-tiktok) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>
- [TikTok terms of service](https://www.tiktok.com/legal/page/row/terms-of-service/en) <br>
- [Metadata reference](artifact/metadata.md) <br>
- [Advanced usage reference](artifact/advanced.md) <br>
- [License terms](artifact/KBLICENSE.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON metadata, and local media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save MP4 videos, info JSON, thumbnails, or archive files locally depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
