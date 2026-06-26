## Description: <br>
Searches academic literature, patents, clinical trials, and related life-science records to investigate biomarkers for diseases, therapies, or specific markers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Life science researchers and pharmaceutical R&D teams use this skill to investigate diagnostic, prognostic, predictive, and pharmacodynamic biomarkers, including associated literature, patents, clinical trials, drug records, targets, and companies. It supports biomarker landscape analysis, patent-risk triage, and structured evidence-backed reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key, and MCP connection URLs can contain that key. <br>
Mitigation: Use a revocable API key, avoid sharing or committing MCP URLs, and rotate the key if exposure is suspected. <br>
Risk: Relevant biomedical, patent, and business research queries are sent to PatSnap MCP services. <br>
Mitigation: Submit confidential or regulated research details only when organizational policy permits that data sharing. <br>
Risk: The skill depends on PatSnap LifeScience MCP connectivity for its primary evidence retrieval. <br>
Mitigation: Verify MCP connectivity before analysis and stop rather than continuing with incomplete tool access. <br>
Risk: Biomarker and patent-risk reports can affect R&D decisions if interpreted without review. <br>
Mitigation: Have qualified scientific, clinical, or legal reviewers validate report conclusions before using them for decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/patsnaplifescience/biomarker-investigation) <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Chemical Molecular MCP Server](https://open.patsnap.com/marketplace/mcp-servers/713886) <br>
- [PatSnap Biology Modality MCP Server](https://open.patsnap.com/marketplace/mcp-servers/06e741) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Dev Portal](https://open.patsnap.com/devportal) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance, Research guidance] <br>
**Output Format:** [Markdown reports with structured sections, citations, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires connected PatSnap LifeScience MCP services for data retrieval; web search is supplemental after MCP retrieval.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact metadata says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
