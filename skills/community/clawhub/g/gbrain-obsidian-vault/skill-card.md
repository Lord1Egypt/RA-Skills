## Description: <br>
Connects an OpenClaw memory directory and gbrain wiki to an Obsidian vault so users can inspect agent memory, entity notes, backlinks, and wikilink graph relationships in one local markdown workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to wire a local gbrain wiki and OpenClaw memory notes into Obsidian for visual graph browsing, backlink review, and markdown-based editing without changing the existing sync and embedding loop. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script overwrites Obsidian app.json and core-plugins.json in the target vault. <br>
Mitigation: Review scripts/setup-vault.sh before running it and back up existing ~/wiki/.obsidian/app.json and core-plugins.json if they contain custom settings. <br>
Risk: The setup links OpenClaw memory notes into the wiki vault, which may expose private daily memory content in Obsidian and local git workflows. <br>
Mitigation: Confirm the memory symlink is acceptable for the user's privacy model and keep the memory path excluded from git with the scripted .gitignore entries. <br>


## Reference(s): <br>
- [Architecture - Obsidian x gbrain x OpenClaw memory](references/architecture.md) <br>
- [Example vault layout](examples/vault-layout.md) <br>
- [ClawHub skill page](https://clawhub.ai/spikesubingrui-design/gbrain-obsidian-vault) <br>
- [Publisher profile](https://clawhub.ai/user/spikesubingrui-design) <br>
- [Obsidian](https://obsidian.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup instructions and can direct the user to run an idempotent shell script that creates a memory symlink, updates gitignore entries, and writes Obsidian configuration files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
