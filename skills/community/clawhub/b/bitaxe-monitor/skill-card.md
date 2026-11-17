## Description:

Monitor Bitaxe Gamma Bitcoin miner status via HTTP API. Use when the user wants to check the status, hashrate, temperature, power consumption, or statistics of a Bitaxe Gamma miner. Supports config file or environment variable for device IP configuration, fetching system info, and formatting output as human-readable text or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pietro395](https://clawhub.ai/user/pietro395)

### License/Terms of Use:


## Use Case:

External users, developers, and Bitcoin mining operators use this skill to configure a Bitaxe miner IP and retrieve status, hashrate, temperature, power, WiFi, pool, uptime, and share statistics from the miner's HTTP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes HTTP requests to a user-configured IP address, so a mistaken or attacker-controlled address could reach sensitive internal HTTP services.

Mitigation: Configure only a trusted Bitaxe or compatible miner IP, preferably on a private LAN, and avoid use in environments where arbitrary internal HTTP access is risky.

## Reference(s):

- [Bitaxe API documentation](https://osmu.wiki/bitaxe/api/)
- [ESP-Miner OpenAPI specification](https://github.com/bitaxeorg/ESP-Miner/blob/master/main/http_server/openapi.yaml)
- [ClawHub skill page](https://clawhub.ai/pietro395/skills/bitaxe-monitor)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Human-readable text or JSON produced by a Python command-line script, with setup and usage commands in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the miner IP from a command argument, local config file, or BITAXE_IP environment variable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
