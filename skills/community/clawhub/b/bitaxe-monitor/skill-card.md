## Description: <br>
Monitor Bitaxe Gamma Bitcoin miner status via HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pietro395](https://clawhub.ai/user/Pietro395) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and Bitaxe users use this skill to configure a miner IP address and retrieve live miner status, including hashrate, temperature, power, fan, WiFi, pool, uptime, and share statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script contacts the HTTP address configured by the user. <br>
Mitigation: Use an IP address for a Bitaxe device you control, preferably on a local network. <br>
Risk: The script can save a miner IP address locally. <br>
Mitigation: Remove ~/.config/bitaxe-monitor/config.json if you no longer want the address saved. <br>


## Reference(s): <br>
- [Bitaxe API Documentation](https://osmu.wiki/bitaxe/api/) <br>
- [ESP-Miner OpenAPI Specification](https://github.com/bitaxeorg/ESP-Miner/blob/master/main/http_server/openapi.yaml) <br>
- [ClawHub Skill Page](https://clawhub.ai/Pietro395/bitaxe-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text status summaries or JSON API data, with Markdown command examples for setup and use.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts the configured Bitaxe HTTP endpoint and can save the miner IP under ~/.config/bitaxe-monitor/config.json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
