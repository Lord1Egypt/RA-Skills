## Description:

Academic Paper Workflow coordinates a seven-stage academic writing process for research, drafting, citation formatting, integrity checks, peer review, final validation, and journal-format outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, academic authors, and research teams use this skill to run a structured paper, grant proposal, or research report workflow with staged checkpoints, citation handling, review, integrity checks, and final formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Academic accuracy and citation integrity can be overstated if workflow goals are treated as guarantees.

Mitigation: Keep human review for citations, evidence, ambiguous references, and final submission decisions, and run the documented integrity checks before relying on outputs.

Risk: Some supporting reference documents are garbled, which can obscure workflow details.

Mitigation: Ask the publisher to repair the reference documents before operational use and prefer clear release evidence, README, and SKILL.md content when reviewing the workflow.

Risk: The workflow creates local output files and checkpoint JSON.

Mitigation: Use an appropriate output directory, confirm filesystem permissions, and review generated files before sharing or submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/academic-paper-workflow)
- [README](README.md)
- [Workflow stages](references/workflow-stages.md)
- [Skill orchestration](references/skill-orchestration.md)
- [Integrity check rules](references/integrity-check-rules.md)
- [IEEE Xplore](https://ieeexplore.ieee.org)
- [Semantic Scholar](https://www.semanticscholar.org)
- [Google Scholar](https://scholar.google.com)
- [arXiv](https://arxiv.org)
- [Web of Science](https://www.webofscience.com)
- [Scopus](https://www.scopus.com)
- [CNKI](https://www.cnki.net)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, JSON, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated workflow artifacts are Markdown, JSON, TXT, DOCX, and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local workflow outputs and checkpoint JSON under a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
