## Description:

Guides OpenClaw through browser-based exchange copy trading by opening a supported venue, entering a follow amount, and confirming the follow-trader flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luyao-inc](https://clawhub.ai/user/luyao-inc)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill with an already logged-in exchange browser session to guide OpenClaw through a Bitget copy-trading follow flow, including amount entry, confirmation, and stopping for manual review when legal or risk acceptance is required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags that the skill can automate a real financial follow-trader action using a packaged default strategy URL and loose URL validation.

Mitigation: Require the user to independently verify the exchange domain, trader, and strategy before automation, and do not treat the packaged default URL as a recommendation.

Risk: The workflow may encounter transaction confirmations, legal acknowledgements, risk prompts, captcha checks, or changed page controls.

Mitigation: Keep final confirmation, legal acknowledgement, and risk acceptance under direct user control, and switch to manual guidance when page controls cannot be reliably located.

## Reference(s):

- [Exchange Copy Trading Reference](artifact/reference.md)
- [ClawHub skill release page](https://clawhub.ai/luyao-inc/skills/exchange-copy-trading)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with browser automation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an already logged-in exchange browser session, sufficient USDT, user-provided amount, and user control over legal acknowledgements and final risk acceptance.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
