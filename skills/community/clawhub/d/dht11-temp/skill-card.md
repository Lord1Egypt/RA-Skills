## Description: <br>
Read temperature and humidity from a DHT11 sensor with configurable GPIO pin selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoahSeeger](https://clawhub.ai/user/NoahSeeger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Raspberry Pi operators use this skill to read DHT11 temperature and humidity measurements from a connected GPIO pin, including custom pin selection through a command-line argument or DHT_PIN environment variable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sudo and Raspberry Pi GPIO access, which can affect the host device if run in the wrong environment. <br>
Mitigation: Install and run it only on the intended Raspberry Pi with the expected DHT11 wiring and GPIO permissions. <br>
Risk: The security evidence identifies a verified output-order bug that may make readings unreliable for automation. <br>
Mitigation: Verify or correct the output order before using the readings in alerts, control loops, or other automation. <br>
Risk: The artifact includes an optional cron example that would run the sensor reader repeatedly in the background. <br>
Mitigation: Add scheduled execution only when continuous logging is intentional and the log path, permissions, and retention are understood. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NoahSeeger/dht11-temp) <br>
- [Publisher profile](https://clawhub.ai/user/NoahSeeger) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Plain text sensor readings and Markdown usage guidance with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Temperature and humidity are printed on separate output lines; the GPIO pin defaults to 19 unless overridden.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
