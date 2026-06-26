## Description: <br>
Complete guide to deploying and optimizing VidAIo SN85 video compression and upscaling miners on Bittensor, including Vast.ai setup, port configuration, NVENC optimization, monitoring, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxquick](https://clawhub.ai/user/maxquick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy, tune, and monitor GPU-backed Bittensor Subnet 85 miners for video compression and upscaling workloads. It is aimed at hands-on miner operations on rented GPU infrastructure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet material may be copied to a rented GPU host. <br>
Mitigation: Use dedicated low-value hotkeys, avoid copying coldkeys or unnecessary wallet files, and rotate keys if the host may be compromised. <br>
Risk: The deployment exposes unauthenticated public miner services. <br>
Mitigation: Expose only the required ports, verify routing, monitor public services, and shut down PM2 startup entries when retiring the host. <br>
Risk: The setup downloads and runs upstream miner code and ffmpeg binaries. <br>
Mitigation: Pin and verify upstream code and binaries before installation, and review changes before updating a production miner. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maxquick/bittensor-sn85-vibe-miner) <br>
- [VidAIo subnet repository](https://github.com/Cazure8/vidaio-subnet) <br>
- [Bittensor documentation](https://docs.bittensor.com) <br>
- [Vast.ai](https://vast.ai) <br>
- [VibeMiner](https://github.com/maxquick/VibeMiner) <br>
- [Optimization history](references/optimization-history.md) <br>
- [Vast.ai port mapping reference](references/port-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands, Python snippets, configuration examples, and operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for an agent to execute or adapt; no structured API output.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
