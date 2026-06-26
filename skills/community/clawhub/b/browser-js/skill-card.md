## Description: <br>
Browser Js provides lightweight Chrome DevTools Protocol browser control for AI agents that need to browse sites, interact with page elements, upload files, capture screenshots, or extract page content with compact command output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaihazher](https://clawhub.ai/user/shaihazher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use Browser Js to automate Chrome or Chromium sessions through CDP for web navigation, form entry, clicking, uploads, screenshot capture, and page-content extraction. It is most useful when an agent needs concise, indexed browser state instead of a large browser snapshot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent CDP-level control over signed-in browser sessions, including clicks, form input, uploads, iframe interactions, screenshots, and page JavaScript evaluation. <br>
Mitigation: Use a separate non-sensitive browser profile, keep the debugging port bound to localhost, and require explicit approval before uploads, purchases, account changes, OAuth/payment/captcha interactions, public posts, or eval commands. <br>
Risk: Coordinate-based commands can interact with UI that is not reachable through indexed DOM elements, including cross-origin iframes and overlays. <br>
Mitigation: Prefer indexed element commands when available and require confirmation for coordinate clicks or drags that affect accounts, payments, captcha flows, posts, or other state-changing actions. <br>


## Reference(s): <br>
- [Browser Js ClawHub release](https://clawhub.ai/shaihazher/browser-js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command output is intentionally compact; page text is capped at 8KB and element HTML is capped at 10KB.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
