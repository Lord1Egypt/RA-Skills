## Description:

Complete a direct browser task, including recovery from blocked sites and an explicit task result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ojusave](https://clawhub.ai/user/ojusave)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to complete direct browser tasks with Playwright-first interaction, coordinate-level fallback, clear limits, credential handling rules, and a verified success or failure result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through account actions, forms, or purchases in a live browser session.

Mitigation: Confirm the exact merchant, item, quantity, fees, and total before approval, and require human completion for authentication challenges.

Risk: Credential, payment, token, address, or phone values could be exposed if handled as ordinary browser text or captured in screenshots.

Mitigation: Use vault handles and vault fill operations for saved secrets, then avoid inspecting filled values or taking screenshots that could reveal them.

Risk: Blocked pages or repeated timeouts could lead to unreliable or open-ended browser attempts.

Mitigation: Use bounded attempts, explicit wait conditions, and a final success or failure result that reports the verified blocker.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ojusave/skills/browser-execution)
- [Server-resolved GitHub provenance](https://github.com/ojusave/openinstinct/tree/main/agent/skills/browser-execution)
- [Kernel browser sessions](https://kernel.sh/docs/introduction/create)
- [Kernel Playwright execution](https://kernel.sh/docs/browsers/playwright-execution)
- [Kernel computer controls](https://kernel.sh/docs/browsers/computer-controls)
- [Kernel live view](https://kernel.sh/docs/browsers/live-view)

## Skill Output:

**Output Type(s):** [Guidance, Code, Text]

**Output Format:** [Markdown or plain text with browser actions, Playwright code, and a terminal success or failure message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require human approval or authentication before completing account actions or transactions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
