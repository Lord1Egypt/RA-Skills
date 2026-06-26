## Description: <br>
Creates, edits, queries, validates, and exports novel character profiles with relationship networks, emotional arcs, and motivation tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Novel-writing agents and developers use this skill to create and maintain structured character profiles during story planning, including roles, relationships, motivations, and growth arcs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project and output path options can read, overwrite, export, or delete local novel project files when pointed at the wrong directory or file. <br>
Mitigation: Use --project and --output only inside the intended novel workspace or a version-controlled folder, and review paths before create, update, export, or delete operations. <br>
Risk: Dependency ranges may reduce reproducibility for installs that require exact repeatability. <br>
Mitigation: Review or pin dependency versions in the installation environment when reproducible installs matter. <br>


## Reference(s): <br>
- [Character Design Guide](references/character_design.md) <br>
- [ClawHub release page](https://clawhub.ai/yuzhihui886/character-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [YAML character files, Markdown exports, and guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads and writes local project files selected by --project and --output.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
