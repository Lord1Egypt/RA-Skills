## Description: <br>
Use the bundled ClawHub Publisher CLI to validate, prepare, zip, and publish OpenClaw skills to ClawHub with clearer validation, cleaner packaging, and safer publish prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sam-k-migz](https://clawhub.ai/user/sam-k-migz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw skill maintainers use this skill to validate local skill folders, prepare cleaned publish-ready bundles, optionally create zip archives, and publish them to ClawHub with confirmation and dry-run support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prepared packages can accidentally include generated bundles or local path details. <br>
Mitigation: Inspect the .clawhub-publisher output before publishing and remove generated archives or local path details that should not be released. <br>
Risk: The publish flow can execute a real ClawHub release, and --yes skips the final confirmation. <br>
Mitigation: Use dry-run or interactive mode first, then use --yes only after confirming the exact package, metadata, and active ClawHub account. <br>
Risk: The server security verdict is suspicious because packaging behavior can expose unintended release contents. <br>
Mitigation: Review the package before installing or publishing with it, and follow the server security guidance for publish workflows. <br>


## Reference(s): <br>
- [ClawHub Publisher release page](https://clawhub.ai/sam-k-migz/clawhub-publisher-cli) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and CLI option values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run commands, validation summaries, prepared bundle paths, zip archive paths, and publish metadata guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
