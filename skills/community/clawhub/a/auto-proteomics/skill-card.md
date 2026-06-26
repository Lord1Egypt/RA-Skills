## Description: <br>
Public OpenClaw skill for low-token routing and downstream analysis of processed DDA LFQ proteomics inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billwanttobetop](https://clawhub.ai/user/billwanttobetop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Auto Proteomics to route eligible processed DDA LFQ protein-level proteomics requests into a narrow two-group downstream workflow. The supported path generates normalized matrices, QC outputs, differential protein tables, reports, summaries, and run manifests from MaxQuant-like processed inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may mistake visible DIA, raw-search, phospho, enrichment, or multi-omics scaffold files for shipped workflows. <br>
Mitigation: Use only the shipped dda-lfq-processed path for normal release use, and frame all other routes as prototype or scaffold material unless later evidence promotes them. <br>
Risk: The public workflow accepts processed proteomics tables and can produce misleading results if input shape, sample mapping, or comparison groups are wrong. <br>
Mitigation: Validate that proteinGroups.txt and summary.txt match the documented DDA LFQ input contract, then review QC outputs and reports before relying on downstream differential results. <br>
Risk: Release staging scripts can write package output to a caller-specified directory. <br>
Mitigation: Run staging only when needed for release work and point any custom output directory at a verified disposable location. <br>


## Reference(s): <br>
- [ClawHub Auto Proteomics page](https://clawhub.ai/billwanttobetop/auto-proteomics) <br>
- [Workflow Index](artifact/references/WORKFLOW_INDEX.yaml) <br>
- [Runtime Requirements](artifact/references/RUNTIME_REQUIREMENTS.md) <br>
- [Demo Input Guide](artifact/references/DEMO_INPUT_GUIDE.md) <br>
- [Branch Framework](artifact/references/BRANCH_FRAMEWORK.md) <br>
- [DIA Input Schema](artifact/references/DIA_INPUT_SCHEMA.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands and generated workflow files, including TSV, JSON, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The shipped public workflow is limited to processed DDA LFQ protein-level inputs and one group-a versus group-b comparison.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
