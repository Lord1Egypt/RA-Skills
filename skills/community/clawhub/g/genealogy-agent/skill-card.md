## Description: <br>
Extract, structure, research, and visualize family history from raw text. Builds knowledge graphs, generates Mermaid trees, Obsidian vaults, and GEDCOM exports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flobo3](https://clawhub.ai/user/flobo3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn family-history text into structured genealogy data, local graph files, Mermaid diagrams, Obsidian notes, and GEDCOM exports, with optional web-assisted ancestor research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Family-history text, names, dates, locations, and research queries may be sent to the configured LLM provider and DuckDuckGo. <br>
Mitigation: Use a dedicated API key with limits, avoid submitting unnecessary sensitive details, and review provider settings before running extraction or research. <br>
Risk: Generated GEDCOM, Markdown, Obsidian, Mermaid, and JSONL outputs may contain sensitive family information. <br>
Mitigation: Write outputs to a private folder and review or delete generated files before syncing, publishing, or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/flobo3/genealogy-agent) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON, JSONL, Markdown, Mermaid, Obsidian vault, and GEDCOM files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files and may call a configured LLM provider and DuckDuckGo during extraction or research workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
