## Description: <br>
Voice and TTS for OpenClaw agents, with spoken replies, optional push-to-talk input, and a local Base wallet for x402 paid calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[forgemeshlabs](https://clawhub.ai/user/forgemeshlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use ClawVoice to add local or hosted agent speech, optional push-to-talk input, and x402 wallet-backed paid voice calls with spend controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and use a local Base USDC hot wallet for x402 payments. <br>
Mitigation: Fund only a small working balance, keep wallet.json private, and use the documented withdrawal path for leftover funds. <br>
Risk: Hosted x402 voice calls can spend wallet funds when automation approves calls. <br>
Mitigation: Keep approval prompts enabled, avoid --approve unless the automation is trusted, and enforce per-call, session, and daily spend caps. <br>
Risk: The push-to-talk conversation mode can pass transcribed speech to a configured agent command. <br>
Mitigation: Configure only agent commands the user would run directly and keep microphone functionality opt-in. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/forgemeshlabs/skills/clawvoice-x402) <br>
- [ForgeMesh Homepage](https://forgemesh.io) <br>
- [Pricing](references/pricing.md) <br>
- [Security](references/security.md) <br>
- [Requirements](references/requirements.md) <br>
- [AgentCash / Poncho Discovery](references/discovery.md) <br>
- [Third-Party Notices](references/third-party-notices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local CLI-driven configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can trigger local audio playback, optional local speech-to-text setup, hosted x402 voice calls, and wallet operations under user-controlled approval and spend caps.] <br>

## Skill Version(s): <br>
0.3.18 (source: SKILL.md frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
