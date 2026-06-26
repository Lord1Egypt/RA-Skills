## Description: <br>
Rust-based Chrome automation for ultra-fast, token-efficient DOM extraction, session management, screenshots, infinite scroll harvesting, and sitemap analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Makforce](https://clawhub.ai/user/Makforce) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to automate Chrome through CDP for navigation, interaction, content extraction, screenshots, session reuse, and MCP-driven browser workflows on authorized sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Powerful browser automation can interact with logged-in sites and dynamic pages. <br>
Mitigation: Use only on authorized sites and run with a separate, isolated Chrome profile. <br>
Risk: Session files, cookies, screenshots, snapshots, local storage, and tab URLs can contain sensitive data. <br>
Mitigation: Treat generated files as secrets, store them securely, and delete them when no longer needed. <br>
Risk: The artifact promotes bot-detection bypass and protected-site scraping recipes. <br>
Mitigation: Avoid bot-evasion workflows and review site terms, authorization, and compliance requirements before use. <br>
Risk: The CLI launches Chrome with sandbox disabled in several commands. <br>
Mitigation: Review the sandbox-disabled behavior before use with logged-in accounts or untrusted web content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Makforce/fast-browser-use-1-0-5) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, screenshots] <br>
**Output Format:** [Markdown guidance with CLI examples; runtime tools return text, Markdown, JSON, and may write PNG or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can preserve browser state through session files and may capture page content, cookies, local storage, screenshots, snapshots, and tab URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
