## Description: <br>
Auto Doc Index helps agents generate README index tables for ADR, RFC, pitfall, and similar documentation files from structured document frontmatter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ERerGB](https://clawhub.ai/user/ERerGB) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and documentation maintainers use this skill to replace hand-maintained README index tables with generated tables derived from individual Markdown files. It is most useful for ADR, RFC, pitfall, design-doc, and similar file-system documentation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator rewrites README content between INDEX markers, so misplaced markers can update the wrong section. <br>
Mitigation: Review the README markers before running the generator and inspect the generated diff before committing changes. <br>
Risk: The documented command uses npx tsx, which can resolve tooling dynamically. <br>
Mitigation: Pin or locally install tsx before running the command when reproducible local tooling is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ERerGB/auto-doc-index) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ERerGB) <br>
- [SkillKit](https://github.com/nicholasbarger/skillkit) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript generator code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generator output rewrites only the README section between INDEX markers.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
