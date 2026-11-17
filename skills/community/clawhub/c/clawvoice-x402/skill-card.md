## Description:

Voice and TTS for OpenClaw agents, with spoken replies, optional push-to-talk input, and a local Base wallet for x402 paid calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forgemeshlabs](https://clawhub.ai/user/forgemeshlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use ClawVoice to add local, hosted, or hybrid voice output, optional push-to-talk input, and x402 wallet controls to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted voice mode can send spoken reply text to a hosted service.

Mitigation: Prefer local mode for confidential content and do not put secrets or private data into text that may be spoken.

Risk: The skill keeps a spend-capable local hot wallet.

Mitigation: Use only small working balances, keep private keys local, and withdraw leftover funds through the explicit withdrawal command.

Risk: Noninteractive approval flags can bypass normal payment or withdrawal prompts.

Mitigation: Avoid --approve and withdrawal --yes unless the automation and destination are fully trusted.

Risk: Voice and microphone installers may install third-party runtime components.

Mitigation: Review install-voice and install-mic before execution and use dry-run or explicit approval flows where possible.

Risk: The configured talk command is executed as a shell command.

Mitigation: Inspect ~/.x402-agent-voice/config.json before using talk and keep agentCommand limited to trusted commands.

## Reference(s):

- [ClawVoice skill page](https://clawhub.ai/forgemeshlabs/skills/clawvoice-x402)
- [ForgeMesh homepage](https://forgemesh.io)
- [Pricing](references/pricing.md)
- [Security](references/security.md)
- [Requirements](references/requirements.md)
- [AgentCash / Poncho Discovery](references/discovery.md)
- [Pyrimid](references/pyrimid.md)
- [Third-Party Notices](references/third-party-notices.md)
- [Supertonic repository](https://github.com/supertone-inc/supertonic)
- [Supertonic 3 model weights](https://huggingface.co/Supertone/supertonic-3)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, audio]

**Output Format:** [Markdown guidance with inline shell commands and optional generated audio output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local voice, microphone, wallet, config, receipt, and audio files under the user's local profile.]

## Skill Version(s):

0.3.18 (source: SKILL.md frontmatter, package.json, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
