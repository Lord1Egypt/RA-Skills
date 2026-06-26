## Description: <br>
Generates Chinese pharmaceutical company profiles with company overview, financing history, pipeline, drug deal, and patent-layout analysis using PatSnap life-science data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patsnaplifescience](https://clawhub.ai/user/patsnaplifescience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to research pharmaceutical companies and produce structured Chinese reports on company background, financing, R&D pipeline, partnerships, and relevant patents. It is intended for workflows connected to PatSnap's life-science MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PatSnap API keys are sensitive credentials. <br>
Mitigation: Use a dedicated or revocable PatSnap API key, avoid placing real keys in shared prompts or files, and rotate the key if exposed. <br>
Risk: Company research or business strategy questions may be shared with PatSnap MCP services and fallback web search providers. <br>
Mitigation: Use the skill only when organizational policy permits sharing that query context, and avoid submitting confidential research or strategy inputs. <br>
Risk: A wrong MCP endpoint or failed connection can prevent reliable analysis. <br>
Mitigation: Verify the PatSnap endpoint and MCP connection status before using the skill for company profiling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/patsnaplifescience/company-profiling-zhcn) <br>
- [PatSnap Open Platform](https://open.patsnap.com) <br>
- [PatSnap Pharma Intelligence MCP Server](https://open.patsnap.com/marketplace/mcp-servers/096456) <br>
- [PatSnap Chemical Molecular MCP Server](https://open.patsnap.com/marketplace/mcp-servers/713886) <br>
- [PatSnap Biology Modality MCP Server](https://open.patsnap.com/marketplace/mcp-servers/06e741) <br>
- [PatSnap Life Science](https://eureka.patsnap.com/ls-landing) <br>
- [PatSnap Developer Documentation](https://open.patsnap.com/devportal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown reports with setup commands and structured sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a PatSnap API key and connected Pharma Intelligence MCP service; may use web search as a fallback after MCP retrieval.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
