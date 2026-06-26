## Description: <br>
EmoPAD Universe helps users locate emotions in the PAD (Pleasure-Arousal-Dominance) coordinate system and provides continuous emoNebula monitoring with periodic emotion nebula chart display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beardao](https://clawhub.ai/user/beardao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this OpenClaw skill to monitor multimodal sensor signals, inspect current PAD emotion status, and generate emotion nebula snapshots from supported EEG, PPG, and GSR devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts background emotion monitoring automatically and reads local sensor data. <br>
Mitigation: Install only in an environment where background monitoring is expected, review the stop command first, and confirm connected sensors and consent requirements before use. <br>
Risk: The skill exposes emotion status through a localhost service on port 8766. <br>
Mitigation: Keep the service bound to localhost, avoid exposing the port externally, and review local API access controls before deployment. <br>
Risk: Dependency installation is automatic and package versions are not pinned. <br>
Mitigation: Review dependencies before installation and prefer a controlled Python environment with approved package versions. <br>
Risk: Broad local process control is used to stop nebula and image viewer processes. <br>
Mitigation: Run in a dedicated user session or controlled environment and review the stop behavior before installing on shared systems. <br>
Risk: PAD emotion calculation is heuristic and does not reflect individual calibration. <br>
Mitigation: Treat PAD outputs as approximate signals, not clinical or individualized assessments, and disclose the lack of personalization to users. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/beardao/emopad-universe) <br>
- [Bilibili demonstration video](https://www.bilibili.com/video/BV1QKPUz7EHV/?spm_id_from=333.337.search-card.all.click) <br>


## Skill Output: <br>
**Output Type(s):** [text, images, shell commands, configuration] <br>
**Output Format:** [Plain text status messages, PNG emotion nebula snapshots, and command-line control output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a localhost service on port 8766 and can open periodic image viewer windows when nebula reporting is active.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
