## Description: <br>
Handles interactions with the dedao-dl CLI tool for listing and downloading Dedao (得到) App courses, ebooks, audiobooks, and related content in formats including PDF, MP3, Markdown, and EPUB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ANGJustinl](https://clawhub.ai/user/ANGJustinl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent list Dedao purchases and download selected courses, articles, ebooks, audiobooks, or notes through the dedao-dl CLI. It is intended for user-authorized management of account-accessible Dedao content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install an unverified third-party dedao-dl binary from GitHub. <br>
Mitigation: Install only with user consent in a trusted environment, and review the release source before executing the binary. <br>
Risk: Cookie-based login can expose Dedao session credentials. <br>
Mitigation: Prefer QR login, avoid pasting session cookies into commands or chats, and keep credentials out of logs. <br>
Risk: Full-course or large downloads can take significant time, consume disk space, or trigger account anti-bot controls. <br>
Mitigation: Require explicit user approval for full-course or large downloads, verify the active Dedao account first, and favor single-article downloads when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ANGJustinl/dedao-dl-skill) <br>
- [dedao-dl GitHub releases API](https://api.github.com/repos/yann0917/dedao-dl/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of downloaded Markdown, PDF, EPUB, HTML, or MP3 files through dedao-dl when the user authorizes downloads.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
