## Description: <br>
Extract quantities from BIM/CAD data for cost estimation. Group by type, level, zone. Generate QTO reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction estimators, BIM specialists, and developers use this skill to process user-provided BIM/CAD exports, group quantities by type, category, and level, and prepare quantity takeoff reports for cost estimation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quantity reports may contain sensitive project information or may be inaccurate if the input BIM/CAD export is incomplete or mapped incorrectly. <br>
Mitigation: Use specific project files, validate inputs, and review generated reports before sharing or using them for cost decisions. <br>
Risk: The skill may read local project files and export reports through a Python data-processing environment. <br>
Mitigation: Run it in a trusted Python environment with reviewed dependencies and write exports only to intended paths. <br>


## Reference(s): <br>
- [Data Driven Construction](https://datadrivenconstruction.io) <br>
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/bim-qto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown tables and summaries, with optional Python code snippets and Excel, CSV, or JSON export guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided BIM/CAD data and should report validation errors clearly before producing reports.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact/claw.json lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
