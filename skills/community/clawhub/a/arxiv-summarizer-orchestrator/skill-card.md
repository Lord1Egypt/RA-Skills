## Description:

Orchestrates end-to-end arXiv paper retrieval, per-paper processing, and batch reporting with language control and parallel or serial paper handling modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xukp20](https://clawhub.ai/user/xukp20)

### License/Terms of Use:


## Use Case:

Developers and research teams use this skill to run a scheduled or manual arXiv literature workflow that collects candidate papers, coordinates per-paper review, and produces a final markdown research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on three separate sub-skills, so an untrusted dependency could affect collection, processing, or reporting behavior.

Mitigation: Install and run only trusted versions of the required collector, paper processor, and batch reporter sub-skills.

Risk: Scheduled runs can accumulate downloaded source files, PDFs, and generated markdown reports over time.

Mitigation: Use a bounded output directory and configure cleanup or retention before enabling periodic execution.

Risk: The workflow downloads external arXiv artifacts and writes local reports.

Mitigation: Review the selected output location and generated files before sharing or automating downstream use.

## Reference(s):

- [Workflow Checklist](references/workflow-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/xukp20/skills/arxiv-summarizer-orchestrator)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and local workflow files, with shell commands for collection, download, bundling, and report rendering steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports an explicit language parameter, serial or bounded parallel per-paper processing, and scheduled runs.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
