## Description: <br>
Uses yt-dlp to help an agent download videos from YouTube, Bilibili, and other supported sites as high-quality MP4 files saved to ~/Movies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frank-gith](https://clawhub.ai/user/frank-gith) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using an agent to save online videos can ask it to download a linked video or playlist with yt-dlp, using high-quality MP4 output and reporting the saved file location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found no artifact-backed concern, but the evidence says target-specific artifact content was not available for a full coherence review. <br>
Mitigation: Install only when the public skill page and source match the intended purpose, and review the skill before relying on it. <br>
Risk: Downloading media from third-party sites may involve restricted content, large files, or login cookies. <br>
Mitigation: Use the skill only for content the user is authorized to download, confirm available disk space, and avoid providing sensitive cookies unless the execution environment is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frank-gith/eye-yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands target yt-dlp downloads to ~/Movies with MP4 merge settings; responses should report errors and saved file locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
