## Description: <br>
Generate ARRIVE 2.0 compliant animal research protocols with structured experimental design, sample size calculations, and reporting checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[theresayao0614-sudo](https://clawhub.ai/user/theresayao0614-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, protocol authors, and review-support teams use this skill to draft and validate ARRIVE 2.0 animal research protocols, reporting checklists, sample-size justifications, randomization plans, and ethics-supporting documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated scientific, statistical, or ethics content may be incomplete or inappropriate for a specific institution, journal, or study design. <br>
Mitigation: Review generated protocols, sample-size rationale, ARRIVE checklist coverage, and ethics material manually before relying on them. <br>
Risk: The skill can read and write local protocol files when the agent is allowed to use local tools. <br>
Mitigation: Install and run it only in workspaces where local protocol file access is acceptable, and inspect files before using generated outputs. <br>


## Reference(s): <br>
- [Arrive Guideline Architect on ClawHub](https://clawhub.ai/theresayao0614-sudo/arrive-guideline-architect-2) <br>
- [ARRIVE 2.0 checklist evidence](artifact/arrive_checklist.md) <br>
- [Example protocol evidence](artifact/example_protocol.md) <br>
- [Example study brief evidence](artifact/example_study_brief.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown protocols and checklists, JSON study briefs, Python-oriented examples, shell commands, and human-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local protocol or checklist files when directed; generated scientific, statistical, and ethics content requires manual review.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
