## Description: <br>
Bulk download TikTok videos from a text file of URLs using yt-dlp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mes28io](https://clawhub.ai/user/mes28io) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a local downloader for batches of TikTok URLs, choose an output folder, and report successful and failed downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs user-directed network downloads and writes video files to a local folder. <br>
Mitigation: Review the URL list before use, select a dedicated download directory, avoid elevated privileges, and download only content you are authorized to save. <br>
Risk: Some TikTok downloads can fail because content is private, deleted, region restricted, or rate limited. <br>
Mitigation: Check the failed URL list, reduce batch size when needed, and retry later only when the download is authorized. <br>


## Reference(s): <br>
- [Upstream README](references/upstream-readme.md) <br>
- [ClawHub skill page](https://clawhub.ai/mes28io/bulk-tiktok-downloader-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local download status summaries, failed URL lists, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
