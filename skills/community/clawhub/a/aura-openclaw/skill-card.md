## Description: <br>
Compile documents into knowledge bases and manage persistent AI agent memory with Aura Core. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[auralithinc](https://clawhub.ai/user/auralithinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to compile local project or document folders into queryable .aura archives and to persist agent memory across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index broad local folders and persist memory, which may capture secrets, credentials, regulated data, or private personal information. <br>
Mitigation: Confirm exact folders before broad indexing requests, avoid storing sensitive data, and use pruning or deletion controls for retained memories. <br>
Risk: Persistent memory may retain outdated or unwanted facts across sessions. <br>
Mitigation: Review stored memory with usage and list commands, prune by date or shard ID, and delete ~/.aura/memory/ when a full reset is needed. <br>


## Reference(s): <br>
- [ClawHub: Aura for OpenClaw](https://clawhub.ai/auralithinc/aura-openclaw) <br>
- [Aura Core](https://github.com/Rtalabs-ai/aura-core) <br>
- [Aura Documentation](https://aura.rtalabs.org) <br>
- [auralith-aura on PyPI](https://pypi.org/project/auralith-aura/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Guidance] <br>
**Output Format:** [Terminal text output, local .aura archives, and memory shard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Python commands, reads user-selected folders or .aura files, and writes local .aura archives or memory data under ~/.aura/memory/.] <br>

## Skill Version(s): <br>
0.1.5 (source: ClawHub release metadata; artifact frontmatter reports 0.1.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
