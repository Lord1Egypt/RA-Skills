## Description: <br>
A guide for reading A-share market and financial data with Baostock and Akshare, including data-source selection, fallback strategies, unit conversion, code-format handling, caching, error handling, R&D expense lookup, and company registration-location lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoy168](https://clawhub.ai/user/zoy168) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts working with A-share data use this skill as a practical reference for choosing Baostock or Akshare interfaces, handling financial-data units and stock-code formats, and applying fallback paths for common data retrieval tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples may query third-party financial data services and may depend on the availability or behavior of those services. <br>
Mitigation: Review the selected data source before use, handle service failures with the documented fallback paths, and validate returned financial data before relying on it. <br>
Risk: Examples may use API tokens or create local cache files when adapted for real workflows. <br>
Mitigation: Keep real tokens out of shared code and logs, and review cache locations and contents before sharing or deploying derived code. <br>
Risk: The skill includes guidance for updating its own troubleshooting notes after repeated attempts. <br>
Mitigation: Review proposed edits before allowing an agent to modify the skill document. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with Python code snippets and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; outputs recommendations, examples, and implementation patterns rather than executing data retrieval directly.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
