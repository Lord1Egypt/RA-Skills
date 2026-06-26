## Description: <br>
A toolkit for migrating or sharing an AI agent's identity, memory, state, relationships, skills, and communication style across environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexlinf](https://clawhub.ai/user/alexlinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to assemble, validate, checksum, and package structured migration files before moving an AI agent to a new environment or sharing it with a trusted recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Migration packs can contain sensitive owner, memory, business, relationship, and agent-state data. <br>
Mitigation: Redact secrets and private owner details before packaging or sharing, and inspect generated archives before sending them anywhere. <br>
Risk: Relationship files may include third-party contact or profiling data. <br>
Mitigation: Include third-party information only with appropriate consent and remove data that is unnecessary for the receiving environment. <br>
Risk: Sharing generated packages can expose sensitive information beyond the local workspace. <br>
Mitigation: Share packs only with trusted recipients and use the included local validation and checksum workflow before transfer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexlinf/agent-migration-pack) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/alexlinf) <br>
- [Author profile](https://friends.coze.site/profile/xiaoyi-linfeng) <br>
- [README](README.md) <br>
- [Migration guide](MIGRATION-GUIDE.md) <br>
- [Changelog](CHANGES.md) <br>
- [Manifest](manifest.toml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON templates and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local migration-pack files and ZIP archives when the included scripts are run.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter, manifest, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
