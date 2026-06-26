## Description: <br>
Query Australian Bureau of Statistics (ABS) datasets via natural language and return live data with citations, tables, JSON or CSV, charts, summaries, and macro snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BillyBodean](https://clawhub.ai/user/BillyBodean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, journalists, researchers, and developers use this skill to find ABS datasets, query Australian economic and demographic time series, and produce cited outputs for reporting or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python scripts that contact the public ABS API and cache ABS metadata locally. <br>
Mitigation: Review the bundled scripts before deployment and run them in an environment where outbound public API access and local cache writes are acceptable. <br>
Risk: Broad ABS queries or use of the all key can return large result sets or require precise SDMX dimension keys. <br>
Mitigation: Prefer validated presets, narrow date ranges, and inspect dataset structure before running unfamiliar direct queries. <br>
Risk: Some datasets are discontinued, stale, or better handled by a dedicated Census workflow. <br>
Mitigation: Follow the skill's replacement guidance for RT and RPPI, and route Census DataPacks or complex Census work to a dedicated census skill. <br>


## Reference(s): <br>
- [ABS Data API Quick Reference Guide](references/api-guide.md) <br>
- [ABS Data API Dataset Catalog](references/dataset-catalog.md) <br>
- [ABS SDMX Dimension Patterns](references/sdmx-patterns.md) <br>
- [ABS Data API](https://data.api.abs.gov.au/rest) <br>
- [ABS Dataflow List](https://data.api.abs.gov.au/rest/dataflow/ABS) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, CSV, PNG charts, shell commands, guidance] <br>
**Output Format:** [Human-readable text, Markdown tables, CSV, JSON with labels, PNG charts, and cited analyst summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include ABS source citations; chart output requires matplotlib and falls back to text when unavailable.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
