## Description: <br>
Downloads and verifies 4K mobile wallpapers from pic.netbian.com using a logged-in cookie, token-based original image downloads, rate-limit spacing, and optional cleanup of non-4K files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guitu917](https://clawhub.ai/user/guitu917) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they explicitly want to batch download mobile wallpapers from pic.netbian.com, preserve only true 4K images, and validate or clean downloaded JPEG files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires copied login cookies, which can expose account credentials if logged, shared, or stored insecurely. <br>
Mitigation: Use only an account and downloads the user is authorized to access, treat cookies like passwords, avoid command history and log exposure, and remove copied cookies after use. <br>
Risk: CAPTCHA or slider handling can become unreliable or violate site controls if automated aggressively. <br>
Mitigation: Keep CAPTCHA and slider completion manual by default; allow at most cautious assistance with explicit user consent, then fall back to manual completion and refresh the cookie. <br>
Risk: Batch downloading may trigger site limits or conflict with the site's terms if run too quickly or at excessive scale. <br>
Mitigation: Respect the site's rate limits and terms, keep the default 180-second interval unless the user has a clear reason to change it, and stop on repeated access failures. <br>
Risk: The cleanup script can delete local JPEG files that do not meet the configured 4K threshold. <br>
Mitigation: Run cleanup only in a controlled wallpaper directory and review the target path before using deletion mode. <br>


## Reference(s): <br>
- [Download Notes](references/download-notes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/guitu917/bian16-wallpaper-downloader) <br>
- [pic.netbian.com](https://pic.netbian.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance with shell commands and downloaded JPEG files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local wallpaper files and console validation results; cleanup can delete non-4K JPEG files when requested.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
