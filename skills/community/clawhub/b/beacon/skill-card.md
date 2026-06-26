## Description: <br>
Bs3 packages Beacon, an agent-to-agent protocol for social coordination, signed messaging, public discovery, P2P mesh transport, and crypto payment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottcjn](https://clawhub.ai/user/scottcjn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Bs3 to coordinate agents across Beacon transports, exchange signed messages, register public identities, and run payment-enabled social or marketplace workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can combine social-account mutation, wallet use, identity management, public discovery, and payment actions. <br>
Mitigation: Run it in a dedicated environment, use least-privileged credentials, prefer dry-run modes first, and avoid storing funded private keys in config. <br>
Risk: UDP, webhook, relay, and Atlas features can expose agent identity, messages, or availability beyond a local test. <br>
Mitigation: Disable Atlas auto-ping and network listeners unless needed, use trusted networks, keep TLS verification enabled, and review retained data under ~/.beacon. <br>
Risk: Security evidence flags weak defaults and overclaims that need review before production use. <br>
Mitigation: Require a security review of configuration, credentials, payment paths, public registration behavior, and retained local state before deployment. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/scottcjn/beacon) <br>
- [Beacon security guide](docs/SECURITY.md) <br>
- [Beacon mechanism test](docs/BEACON_MECHANISM_TEST.md) <br>
- [Beacon dashboard documentation](docs/DASHBOARD.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and command-oriented guidance for configuring and operating Beacon workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce CLI commands, JSON configuration examples, protocol envelopes, and integration guidance.] <br>

## Skill Version(s): <br>
2.16.1 (source: server release metadata, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
