## Description: <br>
Use when the user wants to generate DESIGN.md or design.md from a webpage URL by running a local, rule-based design token extraction script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei1125](https://clawhub.ai/user/liuwei1125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill to extract visible design tokens and component guidance from a user-provided webpage URL or local HTML file before building or restyling UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may capture page metadata, CSS identifiers, and short visible text evidence from pages it analyzes. <br>
Mitigation: Run it only on pages whose local design.md and snapshot outputs may safely contain that information, and avoid sensitive logged-in dashboards, customer data, internal tools, or pages with secrets. <br>
Risk: Generated design tokens are inferred from visible computed styles and may miss hidden states, authenticated views, responsive variants, animation details, proprietary assets, or brand rules that are not visible in the loaded page. <br>
Mitigation: Review the generated design.md before using it as implementation guidance and treat the output as a practical starting point rather than a complete brand book. <br>


## Reference(s): <br>
- [Extraction Rules](references/extraction-rules.md) <br>
- [Design Snapshot Schema](references/snapshot-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown and optional JSON snapshot files, with shell commands for local execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces design.md or DESIGN.md and can optionally write design-snapshot.json for evidence and debugging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
