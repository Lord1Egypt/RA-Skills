## Description:

Browser Harness lets an agent control a user's existing logged-in Chrome browser through CDP to run JavaScript, inspect pages, navigate tabs, click, scroll, take screenshots, fill forms, and upload files while sharing the active browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipingme](https://clawhub.ai/user/sipingme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need an AI agent to work in the same browser session as the user, including authenticated web workflows, page inspection, form entry, screenshots, file upload, and reusable site-specific notes. It is suitable only when the user intentionally wants an agent to control a real Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a real logged-in Chrome session and may expose authenticated pages, personal data, or business data to agent actions.

Mitigation: Install only when this capability is intentional, use a dedicated Chrome profile, and keep BH_PUBLIC_ONLY=1 enabled for public browsing tasks.

Risk: Writes, uploads, screenshots, exec-style commands, and raw browser/CDP control can cause sensitive or irreversible actions.

Mitigation: Require explicit user confirmation before writes, uploads, screenshots, or sensitive-site operations, and avoid exec/raw on sensitive sites.

Risk: The security verdict notes broad exec/CDP escape hatches and safety or upgrade guidance that need review before installation.

Mitigation: Review the skill before use and do not follow @latest or curl-pipe-shell setup shortcuts without a package-verification process.

## Reference(s):

- [Browser Harness Skill on ClawHub](https://clawhub.ai/sipingme/skills/browser-harness-skill)
- [Publisher Profile](https://clawhub.ai/user/sipingme)
- [browser-harness-ts](https://github.com/sipingme/browser-harness-ts)
- [browser-use/browser-harness](https://github.com/browser-use/browser-harness)
- [Browser Use](https://browser-use.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, JSON command output, shell commands, code snippets, and local files such as screenshots or domain-skill notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local screenshot files and metadata-only audit log entries when browser commands run.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
