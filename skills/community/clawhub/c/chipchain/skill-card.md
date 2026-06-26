## Description: <br>
Semiconductor supply chain intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lboquillon](https://clawhub.ai/user/lboquillon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, developers, and research teams use ChipChain to investigate semiconductor materials, equipment suppliers, dependencies, chokepoints, and supply-chain scenarios with sourced multilingual evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional verification scripts can install Python packages and write local verification reports. <br>
Mitigation: Review scripts before running them, execute them in an isolated environment, and inspect generated reports before relying on their results. <br>
Risk: Research workflows may send queries to external search, filing, trade, patent, and financial-data services. <br>
Mitigation: Use approved API keys, avoid placing secrets or sensitive deal details in prompts or queries, and follow the skill's search log and source registry workflow. <br>
Risk: Static semiconductor supply-chain data in the artifact is intended as leads and may be stale or unverified. <br>
Mitigation: Require live source access, confidence labels, a source registry, and a 'What I Could Not Verify' section before treating findings as current. <br>


## Reference(s): <br>
- [ChipChain on ClawHub](https://clawhub.ai/lboquillon/chipchain) <br>
- [Data Sources & API Reference](sources.md) <br>
- [Evidence Types & Confidence Caps](evidence-guide.md) <br>
- [UN Comtrade API](https://comtradeapi.un.org/data/v1/get/C/A/HS) <br>
- [OpenDART API](https://opendart.fss.or.kr/api/) <br>
- [e-Stat API](https://api.e-stat.go.jp/rest/3.0/app/json/) <br>
- [KIPRIS Plus](https://plus.kipris.or.kr) <br>
- [Lens Patent Search API](https://api.lens.org/patent/search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research reports with source registries, confidence labels, search logs, and actionable next steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use declared API keys and optional local verification scripts for ticker, CAS, trade, patent, and filing checks.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
