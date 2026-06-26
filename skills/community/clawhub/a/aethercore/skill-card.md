## Description: <br>
AetherCore v3.3.4 provides local JSON optimization, file indexing, search, and auto-compaction commands for user-specified files and directories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AetherClawAI](https://clawhub.ai/user/AetherClawAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use AetherCore to run local Python commands for JSON performance testing, JSON optimization, smart indexing, search, and auto-compaction on files or directories they explicitly choose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can read, overwrite, and index files or directories that the user points it at. <br>
Mitigation: Run it only on trusted, explicit paths; avoid credential and system directories; keep backups before in-place optimization or compaction. <br>
Risk: Persistent indexes may contain sensitive content from processed files. <br>
Mitigation: Review generated index files and delete or protect them when they include sensitive data. <br>
Risk: The release evidence says the tool overstates safety and its verification script should not be treated as proof of safety. <br>
Mitigation: Inspect the source and dependency set directly, and treat bundled verification output as a limited functional check. <br>


## Reference(s): <br>
- [AetherCore ClawHub page](https://clawhub.ai/aethercore) <br>
- [AetherCore documentation](https://clawhub.ai/aethercore/docs) <br>
- [Security and Scope Declaration](SECURITY_AND_SCOPE_DECLARATION.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create optimized JSON files and persistent index data for user-specified paths.] <br>

## Skill Version(s): <br>
3.3.4 (source: server release evidence, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
