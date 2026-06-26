## Description: <br>
Clack deploys and manages a self-hosted WebSocket voice relay server for OpenClaw, bridging speech-to-text, agent responses, and text-to-speech across local and cloud providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fbn3799](https://clawhub.ai/user/fbn3799) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use Clack to set up secure, self-hosted voice chat with an agent, choose STT/TTS providers, and manage pairing, service, and runtime configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The relay stores sensitive voice context and authentication tokens. <br>
Mitigation: Install only on a server you control, treat the relay token like a password, and avoid shared or multi-user deployments unless users understand transcript and context retention. <br>
Risk: Pairing and authentication controls may be weaker than the documentation suggests. <br>
Mitigation: Firewall port 9878, prefer TLS or Tailscale, and review the generated systemd unit plus config.json permissions before use. <br>


## Reference(s): <br>
- [Clack ClawHub listing](https://clawhub.ai/fbn3799/clack) <br>
- [Clack skill homepage](https://github.com/fbn3799/clack-skill) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Clack iOS app](https://clack-app.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide setup of a systemd-managed relay service and provider credentials.] <br>

## Skill Version(s): <br>
1.5.3 (source: SKILL.md frontmatter, release evidence, CHANGELOG released 2026-02-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
