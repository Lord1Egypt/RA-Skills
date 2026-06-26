## Description: <br>
Browser Harness lets an agent control the user's already-open, logged-in Chrome session through CDP to run JavaScript, click, scroll, capture screenshots, inspect the DOM, fill forms, upload files, and share browser state across Python and TypeScript clients. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sipingme](https://clawhub.ai/user/sipingme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need an agent to inspect or operate the same authenticated Chrome session the user is already using. It supports browser automation tasks such as page inspection, data extraction, form interaction, screenshot capture, file upload, and reusable site-specific guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real logged-in Chrome session, exposing authenticated pages and actions to agent control. <br>
Mitigation: Use it only when that access is intended, prefer a separate Chrome profile, review write and upload commands before execution, and stop the daemon when finished. <br>
Risk: Sensitive sites such as banking, email, internal systems, admin consoles, and health records can contain high-impact data or irreversible actions. <br>
Mitigation: Keep the default sensitive-deny policy enabled, use BH_PUBLIC_ONLY=1 for routine public browsing, and require explicit user approval before any sensitive override. <br>
Risk: Screenshots, DOM reads, and domain-skills notes can capture private data, secrets, or business information. <br>
Mitigation: Keep sensitive data out of screenshots and domain-skills files, and rely on the documented metadata-only audit logging rather than recording page contents. <br>
Risk: Raw browser commands and floating dependency versions can bypass policy controls or change reviewed behavior. <br>
Mitigation: Avoid BH_RAW_OK except for user-approved emergency use, use the normal exec workflow, and keep the pinned browser-harness-ts and browser-harness versions enforced by setup. <br>


## Reference(s): <br>
- [ClawHub Browser Harness Skill Page](https://clawhub.ai/sipingme/browser-harness-skill) <br>
- [Browser Harness README](README.md) <br>
- [Browser Harness API Reference](reference.md) <br>
- [Browser Harness Setup Guide](setup.md) <br>
- [browser-harness-ts](https://github.com/sipingme/browser-harness-ts) <br>
- [browser-use/browser-harness](https://github.com/browser-use/browser-harness) <br>
- [Browser Use](https://browser-use.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON snippets, local file paths, and task result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local screenshots, metadata-only audit entries, and domain-skills files when the user explicitly runs those workflows.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
