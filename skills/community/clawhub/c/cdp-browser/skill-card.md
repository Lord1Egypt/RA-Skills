## Description: <br>
CDP browser control at localhost:9222 for inspecting tabs, taking screenshots, navigating, scrolling, posting to X, and querying page content in a persistent browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gostlightai](https://clawhub.ai/user/gostlightai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to control a local Chrome or Chromium session over CDP, inspect open tabs, extract page text or HTML, capture screenshots, navigate pages, and draft or post approved X content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over logged-in browser tabs. <br>
Mitigation: Use a separate Chrome or Chromium profile with only the accounts and tabs needed, and keep the CDP endpoint local or otherwise protected. <br>
Risk: Page-reading and screenshot commands may expose sensitive page content. <br>
Mitigation: Review page-reading and screenshot requests before execution, store screenshots privately, and delete screenshots after use. <br>
Risk: Posting actions can publish content to X from an authenticated session. <br>
Mitigation: Use tweet-draft as the default, require explicit confirmation for tweet-post, and clear pending tweet files after the workflow completes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gostlightai/cdp-browser) <br>
- [Skill Instructions](SKILL.md) <br>
- [Security Considerations](SECURITY.md) <br>
- [README](README.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, files] <br>
**Output Format:** [CLI output as JSON or plain text; snapshot commands write PNG files; setup guidance uses Markdown and shell snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Chrome or Chromium instance with CDP exposed on localhost:9222 and can operate on logged-in browser sessions.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata, package.json, and changelog dated 2026-02-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
