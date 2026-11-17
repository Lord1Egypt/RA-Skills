## Description:

Helps developers set up a browser-driving agent on a Linux VM, including Xvfb, Chromium launch troubleshooting, access hardening, and egress cost guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to provision and harden a Linux VM for browser-driving agents, troubleshoot headed or headless Chromium failures, and keep browser access, data retention, and egress choices within authorized operating boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provisioning commands can install packages, change services, or alter VM security posture.

Mitigation: Run the skill only on a VM you own or control, and review each sudo, npx, and package-install command before execution.

Risk: A publicly exposed browser gateway, dashboard, or VNC service can expose shell access or logged-in browser sessions.

Mitigation: Keep services bound to loopback and reach them through SSH tunneling or a private mesh network.

Risk: Browser profiles, screenshots, and logs can contain session data or personal data.

Mitigation: Use authorized accounts only, minimize captured data, and install and verify the retention purge described by the skill.

Risk: Disabling Chromium sandboxing reduces browser isolation.

Mitigation: Use no-sandbox mode only on an isolated, disposable VM that accesses authorized targets.

Risk: Browser automation can encounter CAPTCHA, MFA, bot challenges, block pages, rate limits, or geo-gates.

Mitigation: Stop the run and hand off to a human; do not automate bypasses or change egress to route around defenses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/skills/browser-vm-setup)
- [OpenClaw homepage](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with shell commands, configuration snippets, checklists, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a structured provisioning status block for run logs or alerts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
