## Description: <br>
Generate ARRIVE 2.0 compliant animal research protocols with structured experimental design, sample size calculations, and reporting checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and research-support teams use this skill to draft animal-study protocols, ARRIVE 2.0 reporting checklists, and protocol validation summaries for in vivo study planning and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes stronger animal-research compliance, sample-size, IACUC readiness, and animal-welfare claims than the code supports. <br>
Mitigation: Treat outputs as drafting and checklist aids only; require review by a qualified biostatistician and institutional ethics reviewer before using them for study approval, conduct, or publication. <br>
Risk: The bundled CLI writes generated protocols or checklists to caller-provided output paths. <br>
Mitigation: Run the CLI in a dedicated working folder and choose output filenames deliberately before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/arrive-guideline-architect) <br>
- [ARRIVE 2.0 Essential 10 checklist](artifact/arrive_checklist.md) <br>
- [Example generated protocol](artifact/example_protocol.md) <br>
- [Example study brief](artifact/example_study_brief.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown protocols and checklists, plain-text validation summaries, JSON study briefs, and Python or shell usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write protocol or checklist files to user-selected paths when the bundled CLI is run.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
