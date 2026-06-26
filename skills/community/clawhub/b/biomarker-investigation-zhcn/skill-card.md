## Description: <br>
Searches academic and patent literature for biomarker-related evidence based on a user's query. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Life-science researchers and pharmaceutical R&D teams use this skill to investigate disease, target, drug, and biomarker questions with PatSnap life-science MCP data, then produce structured Chinese-language biomarker reports that include literature, patent, clinical, and patent-barrier analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PatSnap API key in the MCP service configuration, and that key-bearing URL can be exposed through copied configuration, shell history, or logs. <br>
Mitigation: Use a dedicated, revocable PatSnap API key and avoid sharing MCP configuration, command output, or logs that include the key-bearing service URL. <br>
Risk: Biomarker and patent-risk conclusions may be used as legal or regulatory decision support outside their evidentiary limits. <br>
Mitigation: Treat outputs as research support, verify cited source records, and route patent-risk or regulatory conclusions through qualified legal or domain review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/patsnaplifescience/biomarker-investigation-zhcn) <br>
- [PatSnap Open Platform](https://open.patsnap.com) <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Developer Documentation](https://open.patsnap.com/devportal) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance, Shell commands] <br>
**Output Format:** [Markdown reports with structured Chinese sections and inline setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured PatSnap life-science MCP service and a revocable PatSnap API key.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
