## Description: <br>
Build or improve AI conference paper workflows by organizing literature, experiment, writing, review, and revision loops into reusable project artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hayashishungenn](https://clawhub.ai/user/hayashishungenn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and developers use this skill to scaffold real AI paper projects, maintain stage-by-stage progress, and coordinate literature review, experiments, drafting, review, and revision without fabricating evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research workflows may run code, install packages, call APIs, or create commits in a live project. <br>
Mitigation: Use a dedicated repository and isolated virtual environment or container, and explicitly approve API calls, package installs, coding-tool invocations, and git commits. <br>
Risk: Paper drafts can become misleading if experiments, citations, datasets, ablations, or statistical tests are invented or not tied to evidence. <br>
Mitigation: Keep the no-fabrication restrictions active, compare claims against logs and result files, and require real citations and real experiment evidence before submission. <br>
Risk: Progress logs and commits can expose credentials or sensitive project information. <br>
Mitigation: Redact secrets from PROGRESS.md and commits before sharing or publishing project artifacts. <br>


## Reference(s): <br>
- [Ai Paper Pipeline on ClawHub](https://clawhub.ai/hayashishungenn/ai-paper-pipeline) <br>
- [Full Pipeline Template](references/full-pipeline-template.md) <br>
- [Project Scaffold](references/project-scaffold.md) <br>
- [Project Mega Prompt Template](templates/MEGA_PROMPT.project.md) <br>
- [Restrictions Example](templates/RESTRICTS.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, LaTeX skeletons, YAML configuration, code project folders, and guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update project scaffolds including MEGA_PROMPT.md, RESTRICTS.yaml, PROGRESS.md, plans, code, data, results, and paper directories.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
