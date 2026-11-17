## Description:

Automates KFC and McDonald's order-link flows by using a configured backend to create order links, drive browser checkout steps, and report order status, pickup codes, and related order information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wananbaby](https://clawhub.ai/user/wananbaby)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to query available KFC or McDonald's products, create food order links through a configured backend, continue supported browser checkout flows, and recover recent local order status when an agent session is interrupted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real food orders and may spend account balance or points if final submission is enabled.

Mitigation: Keep final submission disabled until the user explicitly confirms purchase intent, and test first with controlled accounts or low-risk products.

Risk: The skill sends phone or username values and API keys to a configurable backend.

Mitigation: Install only when the configured backend is trusted, use HTTPS for non-local backends, and prefer scoped or test API keys when available.

Risk: Local order-state outputs can contain usable order links, pickup codes, screenshots, and other sensitive order information.

Mitigation: Protect the order-state output directory, avoid sharing its contents, and delete local outputs when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wananbaby/skills/clawauto-shop)
- [Publisher profile](https://clawhub.ai/user/wananbaby)
- [OpenClaw install checklist](artifact/OPENCLAW_INSTALL_CHECKLIST.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown reports, with command examples and JSON state records for order recovery.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local order-state files, screenshots, order links, pickup codes, and order numbers during supported flows.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
