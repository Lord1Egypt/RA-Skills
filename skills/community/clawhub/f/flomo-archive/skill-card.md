## Description: <br>
Fetches a complete month of Flomo notes and evaluates note quality, using week-to-day fallback to avoid the 50-note search limit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayShna](https://clawhub.ai/user/JayShna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Flomo users use this skill to export all notes for a requested month through a configured local mcporter Flomo MCP server, review summary statistics, and identify low-quality or fragmentary notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The exported /tmp/flomo_YYYY_MM.json file can contain full private note content and metadata. <br>
Mitigation: Review, move, or delete the export after use, especially on shared machines. <br>
Risk: The skill accesses the Flomo account configured in the local mcporter setup. <br>
Mitigation: Install and run it only when the agent is expected to access that Flomo account for the requested monthly export. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JayShna/flomo-archive) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Analysis] <br>
**Output Format:** [Markdown guidance with shell commands; runtime scripts output console summaries and JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports notes to /tmp/flomo_YYYY_MM.json; --json returns structured JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
