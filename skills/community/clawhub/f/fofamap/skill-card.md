## Description: <br>
Use this skill when the user wants FOFA-based asset discovery, host profiling, distribution statistics, icon_hash generation, query refinement after zero-result searches, or cautious follow-up vulnerability triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asaotomo](https://clawhub.ai/user/asaotomo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security analysts, developers, and authorized operators use this skill to turn natural-language reconnaissance goals into FOFA API workflows for asset discovery, host profiling, distribution analysis, recurring monitoring, icon_hash pivots, and cautious follow-up triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires FOFA credentials and can store reconnaissance artifacts locally. <br>
Mitigation: Install only where FOFA credentials and local recon outputs are acceptable, and protect the workspace and environment variables accordingly. <br>
Risk: The skill is intended for reconnaissance and can support live checks or gated Nuclei follow-up. <br>
Mitigation: Use it only for assets you are authorized to investigate, and run Nuclei modes only when active validation is intentional and approved. <br>
Risk: Optional local learning can retain run history and derived patterns. <br>
Mitigation: Set FOFAMAP_DISABLE_LEARNING=1 or configure FOFAMAP_MEMORY_DIR when retained run history is not acceptable. <br>
Risk: FOFA results are indexed intelligence and may be stale, partial, or limited by account permissions. <br>
Mitigation: Call out data limitations in reports, inspect the FOFA permission profile for field-heavy work, and use alive-check only when current reachability changes the decision. <br>
Risk: The security guidance warns against local tool mutation through update behavior unless intentional. <br>
Mitigation: Do not run update commands unless local tool changes are expected and approved for the environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asaotomo/fofamap) <br>
- [Setup](references/setup.md) <br>
- [Query Playbook](references/query-playbook.md) <br>
- [Analysis Playbook](references/analysis-playbook.md) <br>
- [Permission Playbook](references/permission-playbook.md) <br>
- [Monitor Playbook](references/monitor-playbook.md) <br>
- [Redteam Hunt Playbook](references/redteam-hunt-playbook.md) <br>
- [Report Templates](references/report-templates.md) <br>
- [Evolution Playbook](references/evolution-playbook.md) <br>
- [Syntax Arsenal](references/syntax-arsenal.md) <br>
- [Syntax Corpus](references/syntax-corpus.tsv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, code] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper runs may also produce JSON, CSV, XLSX, and Markdown report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local reconnaissance artifacts, monitoring snapshots, report files, and bounded learning artifacts under the configured workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
