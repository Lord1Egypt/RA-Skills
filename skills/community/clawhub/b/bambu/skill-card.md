## Description: <br>
Control Bambu Lab 3D printers (H2D, X1C, P1S, A1) via CLI for print management, AMS filament control, temperature, fans, lights, calibration, file management, and live monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G9Pedro](https://clawhub.ai/user/G9Pedro) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to inspect, configure, and control Bambu Lab printers on a local network. It supports status checks, print operations, AMS management, heating, movement, calibration, file operations, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can issue commands that physically control a 3D printer, including heating, movement, calibration, print start and stop, and raw G-code. <br>
Mitigation: Supervise the printer and require explicit user confirmation before executing physical-control commands. <br>
Risk: LAN access codes and the ~/.bambu/config.json file are sensitive printer credentials. <br>
Mitigation: Keep the access code and configuration file private, and avoid exposing them in logs, prompts, shared files, or screenshots. <br>
Risk: The skill depends on the external @versatly/bambu CLI. <br>
Mitigation: Install and use the CLI only when its package and publisher are trusted for the target environment. <br>
Risk: File deletion and raw G-code commands can cause irreversible printer or job changes. <br>
Mitigation: Confirm target filenames and raw commands before execution, and prefer read-only status commands when diagnosing issues. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/G9Pedro/bambu) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses progressive command loading and distinguishes read-only status commands from physical printer-control commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
