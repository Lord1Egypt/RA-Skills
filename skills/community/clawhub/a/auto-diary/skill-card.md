## Description: <br>
Diary automates daily journaling for OpenClaw by reading configured memory sources, writing a dated diary entry, and exporting a 1080 px image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1204TMax](https://clawhub.ai/user/1204TMax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Diary to generate, archive, and share dated journal entries from configured SOUL, MEMORY, daily memory, and recent diary context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads private memory sources such as SOUL.md, MEMORY.md, daily memory files, and recent diary entries. <br>
Mitigation: Review configured paths before use and limit access to the generated diary directory. <br>
Risk: Generated Markdown and PNG diary outputs may contain private or sensitive personal details. <br>
Mitigation: Treat diary outputs as private until the user reviews and redacts them before sharing. <br>
Risk: A diary entry for the same date could be overwritten if the user asks for regeneration. <br>
Mitigation: Follow the artifact constraint to avoid overwriting existing same-date entries unless the user explicitly requests it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1204TMax/auto-diary) <br>
- [README](artifact/README.md) <br>
- [Initialization Workflow](artifact/INIT.md) <br>
- [Configuration Template](artifact/config.template.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Image files, Configuration] <br>
**Output Format:** [Markdown diary file, PNG image, and a short result summary with date and output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default image width is 1080 px; paths, timezone, and optional news context come from config.yaml.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
