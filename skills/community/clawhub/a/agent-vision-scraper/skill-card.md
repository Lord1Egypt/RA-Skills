## Description:

Agent Vision Scraper runs a Dockerized Playwright browser with virtual display support for vision-assisted web automation, scraping, and CAPTCHA-handling tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tedtalk](https://clawhub.ai/user/tedtalk)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to run browser automation and data extraction workflows in Docker, especially when the task requires visual page interpretation. Users should only apply it to sites they are authorized to automate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags anti-bot automation and CAPTCHA bypass capability as suspicious.

Mitigation: Install and run only when you have explicit permission to automate the target site and the task complies with applicable terms and policies.

Risk: The skill may expose browser activity through VNC and can use credentials or API keys from a .env file.

Mitigation: Bind VNC to localhost or require authentication, avoid shared .env files, and isolate real account credentials.

Risk: Screenshots or page data may be sent to external AI services during vision-assisted browsing.

Mitigation: Avoid sensitive pages unless the external AI service, data handling, and network/container isolation are approved for the data involved.

## Reference(s):

- [Agent Vision Scraper ClawHub listing](https://clawhub.ai/tedtalk/skills/agent-vision-scraper)
- [Tedtalk publisher profile](https://clawhub.ai/user/tedtalk)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime output may include text logs and JSON task results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs through Docker with environment-variable configuration and optional VNC viewing on port 5900.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, package.json, README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
