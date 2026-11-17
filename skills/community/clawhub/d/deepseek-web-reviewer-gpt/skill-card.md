## Description:

GPT-only reviewer workflow for DeepSeek Web using the authenticated ChatGPT Work/Codex Cloud Browser. Requires GPT browser-control; not an OpenClaw-native integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ciklopentan](https://clawhub.ai/user/ciklopentan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to ask DeepSeek Web for an independent review through an authenticated visible browser session, then compare the advisory response with available evidence before making a final decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can transmit selected prompt content or attachments to DeepSeek Web through an authenticated browser session.

Mitigation: Use it only for material authorized for DeepSeek, redact sensitive content where possible, and avoid confidential, regulated, credential, or proprietary data unless the user explicitly approves that transfer.

Risk: DeepSeek responses may be incomplete, incorrect, or in conflict with primary evidence.

Mitigation: Treat DeepSeek output as advisory, classify findings by evidence status, and require the primary agent or user to make the final decision.

Risk: Browser session state, login prompts, CAPTCHA, mode toggles, or UI changes can make the review unreliable.

Mitigation: Verify the visible DeepSeek page, signed-in state, Search mode, and completion status before claiming a review, and stop for manual handoff on authentication or CAPTCHA barriers.

Risk: File upload handling can expose unintended local files if the wrong browser control is targeted.

Mitigation: Upload files only when explicitly authorized, use the visible file chooser flow, and confirm the expected filename appears before sending.

## Reference(s):

- [DeepSeek Web](https://chat.deepseek.com)
- [ClawHub release page](https://clawhub.ai/ciklopentan/skills/deepseek-web-reviewer-gpt)
- [Publisher profile](https://clawhub.ai/user/ciklopentan)

## Skill Output:

**Output Type(s):** [guidance, markdown, analysis]

**Output Format:** [Markdown guidance with classified review findings and brief session status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and should identify confirmed points, candidate claims, conflicts, and unchecked items.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
