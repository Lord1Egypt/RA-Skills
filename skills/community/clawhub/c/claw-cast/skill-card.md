## Description: <br>
Bootstrap and automate OBS scenes for local or remote instances via agentic-obs and mcporter, including baseline scene creation, LAN-served browser overlays, recording walkthroughs, and optional streaming dry runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironystock](https://clawhub.ai/user/ironystock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and stream operators use ClawCast to let an OpenClaw agent bootstrap reusable OBS scene packs, serve local overlay assets, point automation at a local or remote OBS host, and run recording or streaming smoke checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can replace OBS scenes and alter the active OBS scene collection. <br>
Mitigation: Use a disposable OBS scene collection or back up existing scenes before running scene rebuild helpers. <br>
Risk: Recording or streaming helpers can start real OBS output. <br>
Mitigation: Run those helpers only after confirming OBS is pointed at a private test recording or stream target. <br>
Risk: The overlay HTTP server and OBS WebSocket target can expose control or display surfaces if reachable from untrusted networks. <br>
Mitigation: Keep OBS WebSocket and overlay HTTP access limited to a trusted LAN or VPN and verify the target host before execution. <br>
Risk: The target-switch helper writes agentic-obs database configuration. <br>
Mitigation: Provide the DB path only intentionally and keep the explicit cross-component-write acknowledgement requirement in place. <br>


## Reference(s): <br>
- [ClawCast ClawHub page](https://clawhub.ai/ironystock/claw-cast) <br>
- [ClawCast homepage](https://github.com/ironystock/clawcast) <br>
- [Scene Map](references/scene-map.md) <br>
- [Networking Notes](references/networking.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [v0.2.0 Feature Notes](references/v0.2-features.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and bundled HTML, shell, and reference files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may control OBS, update agentic-obs target configuration when explicitly acknowledged, serve browser overlays over local HTTP, and start recording or streaming helpers.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
