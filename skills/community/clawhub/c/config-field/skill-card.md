## Description: <br>
Validate OpenClaw configuration fields against the official Zod schema when reading or writing openclaw.json, including agents, channels, tools, logging, and session settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RedContritio](https://clawhub.ai/user/RedContritio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to validate OpenClaw configuration field paths, inspect field details, and review openclaw.json files before editing, migration, or debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may rely on README placeholder GitHub URLs rather than the verified ClawHub release source. <br>
Mitigation: Install from the verified ClawHub release page or publisher profile, and do not treat placeholder GitHub URLs as provenance. <br>
Risk: The validation scripts may read OpenClaw configuration files, create or update a local schema cache, and check the local OpenClaw version. <br>
Mitigation: Use the skill only on OpenClaw configuration files you intend to validate, and review local cache changes when validating after OpenClaw upgrades. <br>


## Reference(s): <br>
- [OpenClaw Configuration Schema Fields](references/schema-fields.md) <br>
- [ClawHub skill release page](https://clawhub.ai/RedContritio/config-field) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and plain-text validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report field existence, type information, optionality, invalid-field suggestions, and whole-file validation summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
