## Description: <br>
Provides one-click environment initialization, core skill installation, and configuration for OpenClaw users to streamline setup and dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhongchen](https://clawhub.ai/user/wuhongchen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose a local OpenClaw setup, install core skills, configure Feishu and LLM settings, and optionally add persona prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad one-click installation and configuration changes can alter the local OpenClaw environment. <br>
Mitigation: Review the scripts before execution, run in a controlled workspace first, and confirm each external package, hub, or Git source before accepting installs. <br>
Risk: Interactive configuration can write API keys and other secrets to a plaintext .env file. <br>
Mitigation: Enter only secrets approved for local plaintext storage, restrict file access, and rotate keys if the file is exposed. <br>
Risk: Remote installers, Git repositories, and downloaded persona prompts may introduce unreviewed code or instructions. <br>
Mitigation: Verify remote installers and repositories independently, avoid paths intended to bypass login or payment checks, and inspect downloaded persona prompts before using them as system prompts. <br>


## Reference(s): <br>
- [Auto Config Skiller on ClawHub](https://clawhub.ai/wuhongchen/auto-config-skiller) <br>
- [Usage Guide](docs/USAGE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Interactive terminal output with generated configuration files and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local .env and persona.md files and install or update skills from external package, hub, and Git sources.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
