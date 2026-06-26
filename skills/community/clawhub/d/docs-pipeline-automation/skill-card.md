## Description: <br>
Build repeatable data-to-Docs pipelines from Sheets and Drive sources. Use for automated status reports, template-based document assembly, and scheduled publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0x-Professor](https://clawhub.ai/user/0x-Professor) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operations teams use this skill to design repeatable source-to-Google-Docs reporting pipelines and export implementation-ready pipeline specification artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be mistaken for live Google Docs, Drive, or Sheets automation, while security evidence characterizes it as a local planner and export helper. <br>
Mitigation: Treat generated artifacts as pipeline specifications and review them before implementing any real Workspace automation. <br>
Risk: The bundled --dry-run flag does not prevent the script from creating or overwriting the output file. <br>
Mitigation: Use project-local output paths and do not rely on --dry-run as a no-write safeguard. <br>


## Reference(s): <br>
- [Docs Pipeline Guide](references/docs-pipeline-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/0x-Professor/docs-pipeline-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Text guidance plus JSON, Markdown, or CSV pipeline specification files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script accepts optional JSON input, requires an output path, and can write the selected output artifact even when --dry-run is set.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
