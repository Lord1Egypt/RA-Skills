## Description:

A Linux server Chrome browser automation skill for high-resolution screenshots, form filling, login workflows, and Playwright-based stealth automation for sites such as Bilibili and YouTube.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanoha222](https://clawhub.ai/user/kanoha222)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run headless Chrome or Playwright on Linux servers for webpage screenshots and scripted form or login automation on websites they are authorized to automate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill promotes stealth browser automation and anti-bot evasion, which can violate website terms or trigger abuse controls.

Mitigation: Use it only for websites and accounts the operator is authorized to automate, and review site policies before running automated workflows.

Risk: Form and login automation can expose credentials or change account or website state.

Mitigation: Avoid entering real passwords or cookies where possible, use scoped test accounts, and review each automated action before submitting forms.

Risk: The install and browser launch steps include unsafe defaults such as package installation commands and running Chrome without a sandbox.

Mitigation: Run in a sandboxed browser or container, avoid root execution, and prefer pinned dependencies and reviewed install steps.

## Reference(s):

- [Chrome Automation ClawHub release](https://clawhub.ai/kanoha222/skills/chrome-automation)
- [Google Chrome Linux package](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce screenshot files when the generated automation commands or helper script are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
