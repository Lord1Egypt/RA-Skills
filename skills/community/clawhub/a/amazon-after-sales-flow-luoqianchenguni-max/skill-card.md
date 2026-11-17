## Description:

Automates Amazon after-sales by opening orders, accessing details, running contact flow, and drafting or sending seller messages with explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luoqianchenguni-max](https://clawhub.ai/user/luoqianchenguni-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to automate Amazon after-sales workflows, including order lookup, order-detail extraction, contact-flow navigation, and seller message drafting with explicit send confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a live authenticated Amazon browser session and can expose order, page, message, screenshot, or DOM data.

Mitigation: Run it interactively only when that account access is acceptable, review generated messages and artifacts before sharing or retaining them, and keep auto_send off unless sending is deliberate.

Risk: Untrusted JSON inputs could influence browser launch options or navigation targets.

Mitigation: Avoid untrusted JSON inputs and do not pass browser.executablePath or browser.userDataDir.

Risk: Under-scoped navigation controls could direct the browser to attacker-controlled lookalike pages.

Mitigation: Use known Amazon marketplace origins and verify the browser address bar before entering credentials or sending messages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/luoqianchenguni-max/skills/amazon-after-sales-flow-luoqianchenguni-max)
- [README](README.md)
- [Skill Definition](SKILL.md)
- [Skill Manifest](skill.yaml)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON runtime traces and generated message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local artifact paths for screenshots or DOM snippets created during browser automation.]

## Skill Version(s):

0.1.1 (source: server release evidence and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
