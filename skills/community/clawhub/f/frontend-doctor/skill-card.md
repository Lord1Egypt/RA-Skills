## Description:

Diagnose and fix common frontend issues, including white screens, JavaScript errors, resource loading failures, React/Vue hydration problems, browser extension popup failures, and CSS layout bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[727155455](https://clawhub.ai/user/727155455)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend engineers use this skill to diagnose common browser and framework failures in web apps and browser extensions, then produce root-cause, fix, verification, and prevention guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local scanner can read outside the intended project through symlinks.

Mitigation: Run it only on trusted project directories, review symlinks before scanning, and avoid hostile or unknown repositories until symlink boundary checks are added.

Risk: The scanner prints untrusted project text directly to the terminal.

Mitigation: Treat scan output as untrusted, review it before copying commands or reports, and avoid adversarial files until terminal-output sanitization is added.

## Reference(s):

- [Frontend Doctor ClawHub Skill Page](https://clawhub.ai/727155455/skills/frontend-doctor)
- [Publisher Profile](https://clawhub.ai/user/727155455)
- [OpenClaw ClawHub Homepage](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include root-cause analysis, minimal fixes, verification steps, and prevention tips.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
