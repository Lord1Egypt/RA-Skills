## Description: <br>
Extracts media such as videos, photos, GIFs, and audio from social media URLs using yt-dlp across supported platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlacroix82](https://clawhub.ai/user/jlacroix82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and coding agents use Clip Media to inspect, download, or share media from URLs when the user has rights to the content and accepts the exposure risks of downloads, cookies, and optional uploads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public cloud uploads to tmpfiles.org or transfer.sh can expose downloaded media to anyone with the link. <br>
Mitigation: Use local output or --no-upload for sensitive content, and require --confirm-upload before any public upload. <br>
Risk: Browser cookie access can expose active session tokens for sites where the user is logged in. <br>
Mitigation: Use browser cookies only with explicit user consent, prefer non-sensitive public content, and use the narrowest browser profile or credential source available. <br>
Risk: Downloading private, paid, copyrighted, confidential, or regulated content can create account, legal, or privacy exposure. <br>
Mitigation: Confirm the user has rights to the content and avoid private or sensitive sources unless the user intentionally accepts the risk. <br>


## Reference(s): <br>
- [Clip Media on ClawHub](https://clawhub.ai/jlacroix82/clip-media) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, json, shell commands, guidance] <br>
**Output Format:** [Plain text status, local file paths or public URLs, and optional JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads save locally by default; public cloud upload requires explicit --confirm-upload.] <br>

## Skill Version(s): <br>
0.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
