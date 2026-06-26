## Description: <br>
Export the agent core from supported framework repositories into a small source-only zip for AI migration or cross-framework analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Moshiii](https://clawhub.ai/user/Moshiii) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to detect supported agent repositories, extract only agent-defining files, and package those files for migration, portability review, or cross-framework analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated archives may include private agent instructions, memory or context files, configuration details, and absolute local source paths. <br>
Mitigation: Review the generated zip, README.txt, and MANIFEST.txt before sharing or using the export outside the local workflow. <br>
Risk: Running the exporter against unintended repositories can package source files that were not meant for migration or analysis. <br>
Mitigation: Use explicit --base-dir, --repos, and --output-dir values and confirm the target repositories before running the export script. <br>


## Reference(s): <br>
- [Agent Core Design](references/AGENT_CORE.md) <br>
- [AgentPearl homepage](https://github.com/moshiwei/AgentPearl) <br>
- [ClawHub skill page](https://clawhub.ai/Moshiii/agent-core-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the bundled script produces a source-only zip archive with README.txt and MANIFEST.txt.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local repository paths and the zip command when building export archives.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, target metadata, skill frontmatter, and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
