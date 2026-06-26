## Description: <br>
Baoyu Skills is a Claude Code skill bundle for content generation, conversion, publishing, image processing, translation, and web-to-markdown workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[conanwhf](https://clawhub.ai/user/conanwhf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content operators use this bundle to generate images, comics, infographics, slide decks, formatted Markdown, HTML, translations, and social posts from Claude Code workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some subskills can reuse browser sessions, store cookies, automate logged-in account actions, and create drafts or public posts. <br>
Mitigation: Use a dedicated Chrome profile, avoid normal logged-in browser sessions, review account state and generated content before posting, and delete stored cookie or session files when finished. <br>
Risk: Browser debug process termination can affect unsaved browser work. <br>
Mitigation: Do not allow automatic browser-process killing around unsaved work; close or save active browser work before retrying Chrome/CDP automation. <br>
Risk: Image generation and account workflows may require API keys, OAuth tokens, or other credentials. <br>
Mitigation: Use scoped credentials through environment variables or local configuration, rotate them if exposed, and avoid sharing generated logs or files that may contain credential-derived session data. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/conanwhf/baoyu-skills) <br>
- [Chrome Profile](docs/chrome-profile.md) <br>
- [Image Generation Guidelines](docs/image-generation.md) <br>
- [ClawHub / OpenClaw Publishing](docs/publishing.md) <br>
- [Testing Strategy](docs/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and generated file artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some workflows invoke local scripts, browser automation, or external provider APIs and may require Bun, Chrome/CDP configuration, API keys, or logged-in browser sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
