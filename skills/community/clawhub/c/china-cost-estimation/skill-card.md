## Description: <br>
Provides China construction cost estimation, cost composition analysis, and fee calculations based on GB/T 50500-2024, Jianbiao [2013] No. 44, and Jiangsu 2024 fee standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruiyongwang](https://clawhub.ai/user/ruiyongwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cost engineers, project investors, and agents supporting feasibility or preliminary design work use this skill to estimate China construction investment, break down construction and installation costs, and cite applicable standards or rate bases. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Construction cost estimates and referenced rates may be approximate or outdated for financial decisions. <br>
Mitigation: Treat outputs as advisory, verify current standards and rates, and consult qualified cost professionals before investment or procurement decisions. <br>
Risk: The manifest includes a UTF-8 byte order mark that strict JSON parsers may reject. <br>
Mitigation: Remove the byte order mark or use tooling that handles UTF-8 BOMs before automated manifest ingestion. <br>


## Reference(s): <br>
- [China Cost Estimation on ClawHub](https://clawhub.ai/ruiyongwang/china-cost-estimation) <br>
- [Cost Composition Rules](artifact/references/cost-composition-rules.json) <br>
- [Estimation Indices](artifact/references/estimation-indices.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown estimates and analysis with tables and calculation steps; the bundled Python calculator emits plain-text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON reference data; outputs are advisory estimates that should be verified against current standards and rates.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and manifest.json; SKILL.md frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
