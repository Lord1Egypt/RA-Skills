## Description: <br>
Classify construction data by type (structured, unstructured, semi-structured) and recommend appropriate storage, processing, and integration methods. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Construction data practitioners, developers, and project analytics teams use this skill to classify project data sources and choose suitable storage, processing, integration, and quality-control approaches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can analyze local construction or project files and the sample behavior writes a classification_report.md file in the working directory. <br>
Mitigation: Use it only with files intended for analysis, validate input paths, and review export locations before writing reports. <br>
Risk: Storage and processing recommendations may be incomplete or unsuitable for a specific project context. <br>
Mitigation: Review the generated classifications, confidence values, and recommendations before using them for project decisions. <br>


## Reference(s): <br>
- [Data-Driven Construction](https://datadrivenconstruction.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/datadrivenconstruction/data-type-classifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown reports, structured tables, and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May export classification results to Excel, CSV, JSON, or a local classification_report.md file when requested.] <br>

## Skill Version(s): <br>
2.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
