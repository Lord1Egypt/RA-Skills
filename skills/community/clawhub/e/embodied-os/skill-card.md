## Description: <br>
Unified operating system for controlling embodied intelligent robots with AI agents - the control hub bridging AI agents and physical world. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and robotics engineers use this skill to install and apply Embodied-OS guidance for AI-assisted robot control, perception, task planning, and safety configuration. It is intended for agents helping users work with simulated or supervised physical robot systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact physical robot actions. <br>
Mitigation: Use only in simulation or in a supervised, bounded robot workspace until hardware limits, emergency stop behavior, and package behavior are verified. <br>
Risk: The artifact bundles unrelated old video-generator files with extra install and API-use instructions. <br>
Mitigation: Remove or ignore the bundled video-generator files before deployment and review only the Embodied-OS skill path for operational use. <br>
Risk: The skill may submit data to external AI providers through Anthropic or OpenAI API keys. <br>
Mitigation: Use dedicated API keys with spend limits and confirm provider data flows before sending robot, environment, or user data. <br>
Risk: Unreviewed commands could install repositories or run long-running monitoring or robot actions. <br>
Mitigation: Require explicit user confirmation before repository installation, external API submission, long-running monitoring, or any real robot movement. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ZhenStaff/embodied-os) <br>
- [Embodied-OS GitHub Project](https://github.com/ZhenRobotics/openclaw-embodied-os) <br>
- [Embodied-OS PyPI Package](https://pypi.org/project/openclaw-embodied-os/) <br>
- [Embodied-OS npm Package](https://www.npmjs.com/package/openclaw-embodied-os) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Python, YAML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include robot-control setup and execution guidance that should be reviewed before use with physical hardware.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
