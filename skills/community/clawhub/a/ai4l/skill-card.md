## Description: <br>
AI4L helps agents create, audit, iterate, and compare evidence-based Markdown reviews of interventions aimed at health and longevity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[epicoun](https://clawhub.ai/user/epicoun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate structured evidence reviews, run QA audits against the AI4L checklist, and revise Markdown review files based on audit results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The VERIFY workflow can revise Markdown documentation and agent-instruction files without a clear confirmation boundary. <br>
Mitigation: Run VERIFY only in the intended project directory and require review or explicit confirmation before accepting edits to SKILL.md, CLAUDE.md, PERSONA.md, README.md, docs, or examples. <br>
Risk: Automated audit and fix workflows may update evidence review files based on model-generated judgments. <br>
Mitigation: Review generated ER and QA Markdown outputs before relying on them for practical longevity decisions or publishing them. <br>
Risk: The skill may use web tools, sub-agents, and a local counting script during review workflows. <br>
Mitigation: Use the skill in a controlled workspace and review requested tool use, generated files, and script execution before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/epicoun/ai4l) <br>
- [AI4L QA guideline](artifact/AI4L.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown files and concise text status reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated evidence reviews and QA audit files under ./results/.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
