## Description: <br>
Help develop, build, flash, and debug ESP32/ESP8266 firmware using Espressif ESP-IDF on Linux/WSL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[547895019](https://clawhub.ai/user/547895019) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and firmware engineers use this skill to work through ESP-IDF setup, target configuration, builds, flashing, serial monitoring, component management, WSL USB serial attachment, and firmware packaging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can flash devices and manage USB attachment from WSL, which can affect connected hardware or the host USB state. <br>
Mitigation: Use trusted ESP-IDF installs and project build directories, prefer --list and --dry-run before attachment, and specify exact ports or devices. <br>
Risk: Generated firmware packages and flash scripts may be distributed or run outside the original build environment. <br>
Mitigation: Review generated flash packages before running or distributing them, and confirm the intended firmware binaries, ports, and devices. <br>


## Reference(s): <br>
- [ESP-IDF](https://github.com/espressif/esp-idf) <br>
- [ESP Component Registry](https://components.espressif.com/components) <br>
- [idf.py help reference](references/idf-py-help.txt) <br>
- [ClawHub skill page](https://clawhub.ai/547895019/esp-idf-helper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May refer users to bundled shell scripts for capturing idf.py help, attaching WSL USB serial devices, and packaging firmware.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
