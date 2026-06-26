## Description: <br>
Observability pipeline and CI audit pack for JSONL-to-SQLite trace ingestion and CI workflow validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill to ingest JSONL traces into SQLite for analysis and to check CI workflow configurations for security gates and test steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using an untrusted or unexpected mcp-openclaw-extensions package version could expose the agent to unsafe tool behavior. <br>
Mitigation: Install only trusted mcp-openclaw-extensions versions that satisfy the declared requirement and review the package before deployment. <br>
Risk: Trace logs and generated SQLite databases may contain sensitive operational data or secrets. <br>
Mitigation: Use scoped trace inputs, avoid logs containing secrets where possible, and store generated SQLite databases in protected locations. <br>


## Reference(s): <br>
- [Firm Observability Pack on ClawHub](https://clawhub.ai/romainsantoli-web/firm-observability-pack) <br>
- [romainsantoli-web publisher profile](https://clawhub.ai/user/romainsantoli-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline tool commands, analysis summaries, and validation findings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reference a SQLite database from scoped JSONL trace input; requires mcp-openclaw-extensions >= 3.0.0.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
