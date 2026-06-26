## Description: <br>
Run local ExpertPack CLI tools for validating, fixing, graphing, and deploying packs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run ExpertPack validation, repair, graph export, frontmatter stripping, and deployment-prep commands against local pack files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to run tools from a separate local ExpertPack repository. <br>
Mitigation: Confirm that the local ExpertPack repository is trusted before running its tools. <br>
Risk: Doctor and wikilink-fix commands can modify local pack files when apply flags are used. <br>
Mitigation: Run dry-run modes first and inspect proposed changes before applying fixes. <br>
Risk: Adding pack paths to OpenClaw memory search can make local pack content available for retrieval. <br>
Mitigation: Add only intended pack paths to memory search configuration. <br>


## Reference(s): <br>
- [ExpertPack CLI Commands Reference](references/cli-commands.md) <br>
- [ClawHub ExpertPack CLI Release](https://clawhub.ai/brianhearn/expertpack-cli) <br>
- [ExpertPack Tool Repository](https://github.com/brianhearn/ExpertPack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides local-file operations and does not bundle executable tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
