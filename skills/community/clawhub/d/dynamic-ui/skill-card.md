## Description: <br>
Render tables, charts, stats, cards, and dashboards as images using HTML templates and wkhtmltoimage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theashbhat](https://clawhub.ai/user/theashbhat) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to turn structured JSON data into shareable PNG visuals such as tables, bar charts, KPI summaries, information cards, and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering user-provided data and optional remote image URLs can expose sensitive content or fetch external resources. <br>
Mitigation: Avoid rendering secrets unless needed, review image URLs before use, choose output paths deliberately, and delete generated files when they are no longer needed. <br>
Risk: The renderer enables JavaScript while converting HTML to PNG. <br>
Mitigation: Disable JavaScript or run rendering in an isolated environment when stricter execution controls are required. <br>


## Reference(s): <br>
- [Dynamic UI ClawHub page](https://clawhub.ai/theashbhat/dynamic-ui) <br>
- [OpenClaw](https://openclaw.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [PNG image files or base64-encoded PNG output from shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses JSON input, selectable templates, selectable themes, optional output path, and configurable image width.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
