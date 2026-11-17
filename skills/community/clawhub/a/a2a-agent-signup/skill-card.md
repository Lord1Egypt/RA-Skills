## Description:

Interactive CLI wizard for onboarding an agent to the A2A Marketplace by collecting wallet, profile, service, payment, and registration details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcus20232023](https://clawhub.ai/user/marcus20232023)

### License/Terms of Use:


## Use Case:

Developers and service providers use this skill to register an agent profile, optionally create an initial service listing, and submit payment proof for A2A Marketplace onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation can persistently modify the user's shell PATH and create a command symlink.

Mitigation: Review setup.sh and package postinstall behavior before installation, and remove unwanted PATH or symlink changes after testing.

Risk: The CLI stores wallet and authentication data locally.

Mitigation: Run it only in a trusted environment, keep generated .env files out of source repositories, and protect ~/.a2a-agent-config.

Risk: Using an untrusted A2A_API_URL can expose users to command execution through the browser-opening payment path.

Mitigation: Use the default trusted endpoint unless the browser-opening command injection issue has been fixed and the alternate endpoint is trusted.

Risk: The signup flow charges a small USDC registration fee to a documented wallet.

Mitigation: Confirm the fee amount, recipient wallet, and Polygon network before submitting payment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marcus20232023/skills/a2a-agent-signup)
- [A2A Marketplace](https://a2a.ex8.ca)
- [A2A JSON-RPC endpoint](https://a2a.ex8.ca/a2a/jsonrpc)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, JSON]

**Output Format:** [Terminal prompts and status text, shell setup commands, local JSON configuration, and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write .env in the current directory and ~/.a2a-agent-config in the user's home directory.]

## Skill Version(s):

1.2.4 (source: server release version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
