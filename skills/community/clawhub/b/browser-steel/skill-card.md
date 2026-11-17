## Description:

Browser Steel enables agents to automate JS-heavy sites through Steel CLI by default, with a Python Playwright fallback for custom browser flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyanmi](https://clawhub.ai/user/xyanmi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture live page content, screenshots, PDFs, fill forms, manage named browser sessions, and debug login, CAPTCHA, and browser workflows on authorized sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an unpinned downloaded Steel CLI through the npx fallback.

Mitigation: Prefer a preinstalled, pinned Steel CLI and run the doctor command before browser automation.

Risk: Browser automation can access local environment, cookie, profile, and session material.

Mitigation: Run with a minimal environment, keep unrelated secrets out of workspace .env files, and provide cookie, profile, and session inputs only for accounts and sites the user is authorized to automate.

Risk: Automated interaction with login, CAPTCHA, and form workflows can act on sensitive or unauthorized sites.

Mitigation: Use the skill only for authorized accounts and sites, review each workflow before execution, and avoid blind retries when anti-bot friction appears.

## Reference(s):

- [Browser Steel ClawHub release](https://clawhub.ai/xyanmi/skills/browser-steel)
- [Official Steel CLI overview](https://docs.steel.dev/overview/steel-cli)
- [Steel agent-friendly docs index](https://docs.steel.dev/llms-full.txt)
- [Playwright + Steel Python guide](https://docs.steel.dev/overview/guides/playwright-python)
- [Runtime modes reference](references/runtime-modes.md)
- [CLI workflows reference](references/cli-workflows.md)
- [Python plan runner reference](references/python-plan.md)
- [Troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and optional JSON, screenshot, or PDF artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STEEL_API_KEY for Steel-backed runtime; may use Steel CLI, npx @steel-dev/cli, or Python Playwright plan execution.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
