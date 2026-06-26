## Description: <br>
Orchestrates end-to-end arXiv paper retrieval, processing, and batch reporting with language control and parallel or serial paper handling modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xukp20](https://clawhub.ai/user/xukp20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and research teams use this skill to run a complete arXiv literature collection workflow, from focused query planning through per-paper summaries and a final collection report. It is intended for scheduled or manual research-monitoring workflows that need language-controlled Markdown outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on three required arXiv sub-skills that perform collection, paper processing, and reporting. <br>
Mitigation: Install and enable only trusted versions of arxiv-search-collector, arxiv-paper-processor, and arxiv-batch-reporter before using this orchestrator. <br>
Risk: Concurrent paper processing can create file conflicts or excessive external requests if limits are ignored. <br>
Mitigation: Keep paper processing within the documented parallelism limit, use one worker per paper directory, and use the documented fetch throttling and retry controls. <br>
Risk: Scheduled runs can repeatedly collect and write arXiv outputs without direct supervision. <br>
Mitigation: Enable cron or scheduled execution only when recurring automated collection is intended, and run the workflow in a dedicated output directory. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xukp20/arxiv-summarizer-orchestrator) <br>
- [Workflow Checklist](references/workflow-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON run metadata, and shell commands for arXiv collection, paper processing, and batch reporting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a run directory containing task metadata, query results, paper metadata, per-paper summaries, summary bundles, report templates, and a final collection report.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
