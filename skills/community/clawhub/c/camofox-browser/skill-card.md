## Description: <br>
Headless browser automation server enabling AI agents to create tabs, navigate, interact with pages, manage sessions, import cookies, capture snapshots, screenshots, images, downloads, and YouTube transcripts through a local or cloud-hosted Camoufox service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheffk78](https://clawhub.ai/user/sheffk78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give AI agents controlled browser automation for web navigation, page interaction, accessibility snapshots, screenshots, downloads, image extraction, cookie-backed sessions, proxy-aware browsing, and transcript retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-start a powerful local browser automation server with broad page interaction controls. <br>
Mitigation: Disable auto-start unless needed, and bind or firewall the server so only trusted local clients can reach it. <br>
Risk: Cookie import can give an automated browser access to authenticated user sessions. <br>
Mitigation: Set CAMOFOX_API_KEY before using cookies, import only cookies intended for automation, and require explicit confirmation before actions on logged-in accounts. <br>
Risk: Raw page scripting, account actions, purchases, posting, settings changes, and session deletion can have high impact. <br>
Mitigation: Require user confirmation before high-impact browser actions and before deleting sessions or user data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sheffk78/camofox-browser) <br>
- [Camoufox](https://camoufox.com) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Images, Files, API responses, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON API examples, accessibility snapshots, base64 screenshots or downloads when requested, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return browser element references, tab and session identifiers, image metadata, transcript text, and captured download data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
