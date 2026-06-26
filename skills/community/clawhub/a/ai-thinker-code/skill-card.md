## Description: <br>
Ai-Thinker-Coder guides agents through Ai-Thinker IoT module development across WiFi, BLE, LoRa, radar, NB-IoT, and NearLink module families, with chip-specific sub-skills for detailed workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seahi-mo](https://clawhub.ai/user/seahi-mo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill as an entry point for selecting Ai-Thinker module families, installing chip-specific sub-skills, setting up development tools, and following build and firmware flashing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users to clone SDKs and run build scripts from external repositories. <br>
Mitigation: Verify repository URLs and inspect cloned SDK scripts before running builds. <br>
Risk: USB passthrough and firmware flashing commands can affect connected hardware or the wrong serial device. <br>
Mitigation: Confirm the target USB bus ID and serial device before binding, attaching, or flashing firmware. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seahi-mo/ai-thinker-code) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/seahi-mo) <br>
- [Ai-Thinker website](https://www.ai-thinker.com) <br>
- [Ai-Thinker documentation center](https://docs.ai-thinker.com) <br>
- [Ai-Thinker technical support forum](https://bbs.ai-thinker.com) <br>
- [Ai-Thinker Open GitHub organization](https://github.com/Ai-Thinker-Open/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, setup steps, reference links, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hardware setup and firmware flashing guidance that should be checked against the selected module and serial device.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
