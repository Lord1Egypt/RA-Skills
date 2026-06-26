## Description: <br>
Adaptive, auditable research across web sources, papers, GitHub projects, documentation, datasets, and local files for cited answers and evidence-backed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b143kc47](https://clawhub.ai/user/b143kc47) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, analysts, and external users use this skill for multi-source research, literature review, project due diligence, claim verification, and cited decision support when simple lookup is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research runs may browse external sources and encounter prompt-injection attempts or misleading source material. <br>
Mitigation: Treat source content as untrusted, verify high-impact claims with primary or independent sources, and preserve citations or evidence IDs for auditability. <br>
Risk: Research notes or ledger files may capture sensitive information if users include secrets or unnecessary personal data in prompts, paths, or excerpts. <br>
Mitigation: Keep run directories in a controlled workspace and avoid logging credentials, tokens, private data, or unrelated personal information. <br>
Risk: Reset or cleanup actions could remove research artifacts from an unintended directory. <br>
Mitigation: Use reset only on directories created for the research run and confirm the target path before cleanup. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/b143kc47/b143kc47-deep-research) <br>
- [Publisher Profile](https://clawhub.ai/user/b143kc47) <br>
- [Project Homepage](https://github.com/B143KC47/deep-research-skill) <br>
- [Adaptive Deep Research Protocol](references/research-protocol.md) <br>
- [Source Quality Guide](references/source-quality.md) <br>
- [Query Playbook](references/query-playbook.md) <br>
- [Project and Paper Research Patterns](references/project-and-paper-patterns.md) <br>
- [Report Template](references/report-template.md) <br>
- [Evaluation Checklist](references/evaluation.md) <br>
- [OpenClaw Installation Notes](references/openclaw-install.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research responses and reports with evidence IDs, citations, tables, and optional shell command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local research ledger files in a writable workspace when the bundled Python script is used.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
