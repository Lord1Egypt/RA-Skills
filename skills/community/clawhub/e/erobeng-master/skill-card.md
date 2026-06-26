## Description: <br>
Query the Cancer Dependency Map (DepMap) for cancer cell line gene dependency scores, drug sensitivity data, and gene effect profiles to support cancer vulnerability, synthetic lethality, and oncology target validation analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erisonbarros](https://clawhub.ai/user/erisonbarros) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, bioinformaticians, and developers use this skill to query and analyze DepMap cancer dependency, gene effect, mutation, expression, and drug sensitivity data. It supports target validation, biomarker discovery, synthetic lethality exploration, and co-essentiality analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release metadata and artifact contents do not fully align, including skill naming and license signals. <br>
Mitigation: Confirm the intended package identity, publisher, and license terms before relying on or redistributing the skill. <br>
Risk: Example workflows can access public DepMap or Figshare resources and download large CSV datasets. <br>
Mitigation: Review data sources, storage location, and download size before running examples in constrained or regulated environments. <br>
Risk: Cancer dependency scores and statistical examples can be misinterpreted as validated therapeutic conclusions. <br>
Mitigation: Treat outputs as research support and validate findings with domain review, multiple-testing correction, and independent evidence before decision-making. <br>


## Reference(s): <br>
- [DepMap Portal](https://depmap.org/portal/) <br>
- [DepMap Data Downloads](https://depmap.org/portal/download/all/) <br>
- [DepMap API](https://depmap.org/portal/api/) <br>
- [DepMap Portal GitHub Repository](https://github.com/broadinstitute/depmap-portal) <br>
- [DepMap 24Q4 Public Figshare Dataset](https://figshare.com/articles/dataset/DepMap_24Q4_Public/27993966) <br>
- [DepMap Dependency Analysis Guide](references/dependency_analysis.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and analysis workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference public DepMap or Figshare resources and may guide users through large local CSV downloads for larger analyses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
