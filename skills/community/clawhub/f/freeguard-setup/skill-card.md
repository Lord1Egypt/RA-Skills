## Description: <br>
Guide users through installing, signing in to, connecting, and troubleshooting FreeGuard VPN with the official FreeGuard CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jojocrystal](https://clawhub.ai/user/jojocrystal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to set up and operate FreeGuard VPN through the official CLI, including installation checks, sign-in, subscription status, connection, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow may involve sensitive account data, subscription checkout, or access tokens. <br>
Mitigation: Ask for explicit user confirmation before account or billing actions and direct users to enter credentials, verification codes, and payment details only through the FreeGuard CLI or official browser flow. <br>
Risk: System-wide VPN routing can change local network behavior and may require administrator approval. <br>
Mitigation: Default to the standard non-elevated connection flow and discuss system-wide protection only when the user explicitly asks for it. <br>
Risk: The skill depends on an external VPN CLI and service that are outside the skill package. <br>
Mitigation: Install only from the official FreeGuard source, verify the CLI with diagnostic commands, and use checksum-verified release assets when Homebrew is unavailable. <br>


## Reference(s): <br>
- [FreeGuard VPN homepage](https://freeguardvpn.com) <br>
- [ClawHub skill page](https://clawhub.ai/jojocrystal/freeguard-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; account, billing, and network-routing actions are performed by the FreeGuard CLI after user confirmation.] <br>

## Skill Version(s): <br>
0.8.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
