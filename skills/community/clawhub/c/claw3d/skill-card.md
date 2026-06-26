## Description: <br>
Unified 3D workflow: create models (AI), search (Thingiverse), slice, print. Modular-enable only what you need. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makermate](https://clawhub.ai/user/makermate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and 3D-printing operators use this skill to guide an agent through model creation or search, previewing, slicing, and printer control with the claw3d CLI. The skill supports modular workflows for AI generation, Thingiverse search, CuraEngine slicing, and Moonraker or PrusaLink printing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to control physical 3D printers and issue print, start, preheat, home, cancel, or emergency-stop commands. <br>
Mitigation: Use only in an environment where the operator trusts the agent with printer control, and require manual confirmation before any printer-control action. <br>
Risk: The skill includes guidance for persistent OpenClaw configuration changes, including increasing Telegram media limits. <br>
Mitigation: Apply persistent configuration changes only with administrator approval and after reviewing the impact on the deployment. <br>
Risk: Generated or downloaded models may be unsuitable for a printer, build volume, or intended physical use. <br>
Mitigation: Review previews, dimensions, slicing estimates, and printer profile settings before printing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makermate/claw3d) <br>
- [OpenClaw 3D homepage](https://github.com/makermate/openclaw-3d) <br>
- [Thingiverse app token setup](https://www.thingiverse.com/apps/create) <br>
- [FAL API key dashboard](https://fal.ai/dashboard/keys) <br>
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands, file paths, and generated 3D workflow artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference GLB, STL, G-code, preview video, configuration, and printer-control outputs through the claw3d CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
