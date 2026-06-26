## Description: <br>
Load CSV files and ask questions in plain English. AI-powered natural language queries via Anthropic, OpenAI, or local Ollama. No SQL required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and data analysts use this skill to load CSV or TSV files, profile columns, run structured filters or aggregations, and ask natural-language questions about tabular data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud AI modes can send CSV-derived metadata and sample rows to Anthropic or OpenAI. <br>
Mitigation: Use local Ollama, redact sensitive columns and sample rows, or obtain approval before using cloud providers with confidential, regulated, customer, or secret-bearing CSVs. <br>
Risk: AI-generated answers may be inaccurate for important analysis. <br>
Mitigation: Manually verify important results against the underlying data or a structured query before relying on them. <br>


## Reference(s): <br>
- [CSVBrain ClawHub Page](https://clawhub.ai/TheShadowRose/csv-brain) <br>
- [TheShadowRose Publisher Profile](https://clawhub.ai/user/TheShadowRose) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, guidance] <br>
**Output Format:** [Plain English answers and JSON objects from JavaScript APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Anthropic, OpenAI, or local Ollama when natural-language questions are used; structured query and profile operations run locally.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
