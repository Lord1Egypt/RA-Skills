## Description:

AI-assisted short video creation workflow where the user selects topic, aspect ratio, and duration, then receives guided video-generation support using the user's own third-party API key after a one-time payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

External creators use this skill to run a paid, guided short-video creation workflow. It helps them choose video parameters, configure their own Kling or Doubao-style video-generation API credentials, and receive resulting video guidance and suggested copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment authorization is weak because local order files can be edited to forge verification.

Mitigation: Review the payment gate before installation and rely only on trusted payment verification for paid use.

Risk: Payment metadata may be stored in plaintext when SM4 encryption is not configured or encryption fails.

Mitigation: Configure CLAWTIP_SM4_KEY correctly and treat encryption warnings as a reason to stop using the paid workflow until resolved.

Risk: The skill guides use of third-party video APIs rather than shipping a complete video-generation backend, and users may provide API keys to those providers.

Mitigation: Use only trusted third-party video providers, scope credentials where possible, and rotate or revoke keys if exposure is suspected.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jinyu12166/skills/ai-video-creator-assistant)
- [Kling AI](https://klingai.com)
- [Volcengine](https://www.volcengine.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit order number, amount, indicator, payment status, video-generation guidance, video link, and recommended copy; relies on user-provided third-party video API credentials.]

## Skill Version(s):

1.0.1 (source: evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
