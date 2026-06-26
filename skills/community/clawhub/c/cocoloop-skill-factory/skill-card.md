## Description: <br>
CocoLoop Skill Factory helps agents turn rough skill ideas into stable multi-platform Agent Skill specs, implementation plans, templates, and release boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[catrefuse](https://clawhub.ai/user/catrefuse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this meta-skill to create, upgrade, migrate, or package Agent Skills across platforms such as Codex, Claude Code, OpenClaw, Copaw, Molili, and Hermes Agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can search external registries and fetch reference skills, which may introduce untrusted source material into the skill-building workflow. <br>
Mitigation: Review fetched reference skills and provenance before reuse, and keep external search results as evidence rather than executable instructions. <br>
Risk: Generated or bundled scripts may install dependencies, write files, package artifacts, or guide browser/session automation. <br>
Mitigation: Review dependency installs, output paths, generated commands, implicit-invocation settings, and browser automation steps before execution. <br>
Risk: The release is tagged with sensitive capability indicators such as OAuth tokens, sensitive credentials, purchases, and crypto. <br>
Mitigation: Confirm whether the target skill actually needs each sensitive capability and remove unnecessary permissions or credential-handling steps before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/catrefuse/cocoloop-skill-factory) <br>
- [CocoLoop Skill Factory Instructions](artifact/SKILL.md) <br>
- [Atomic Capability Index](artifact/atomic-capability/index.md) <br>
- [Factory Skill Builder README](artifact/factory-skill-builder/README.md) <br>
- [Platform Support Matrix](artifact/ref/platform-support-matrix.md) <br>
- [Preset Index](artifact/presets/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with generated files, configuration snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce skill specs, build plans, platform manifests, validation guidance, and packaged skill artifacts depending on the target platform.] <br>

## Skill Version(s): <br>
0.3.5 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
