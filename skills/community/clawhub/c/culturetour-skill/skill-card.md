## Description: <br>
Helps agents search the data0086.com culture-tourism media catalog, present previewable results, support selection and purchase-style commands, and download selected videos after the configured mock or trade flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengyily](https://clawhub.ai/user/fengyily) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting tourism, media, or content teams use this skill to search Chinese culture-tourism video materials, compare finished clips and raw materials, preview assets, and download selected videos after an explicit purchase or down-order command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Purchase or down-order chat commands can immediately download remote media into local storage without a separate confirmation step. <br>
Mitigation: Use the skill only where this behavior is acceptable, keep downloads constrained to a dedicated folder, and add an explicit confirmation step before deployment if local writes require stronger user control. <br>
Risk: Misconfigured media or trade endpoints could expand where the agent sends requests or downloads files from. <br>
Mitigation: Review WENLV_API_ORIGIN, TRADE_API_BASE, and trusted_media_origins before use, and preserve the origin checks in the download script. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/fengyily/culturetour-skill) <br>
- [API Interface Specification](api.md) <br>
- [Culture-Tourism Search API Reference](references/api_reference.md) <br>
- [data0086 Platform](https://www.data0086.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [HTML or Markdown tables with preview links, optional JSON details, shell download commands, and local file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are capped by the skill flow, media embedding is limited to configured trusted origins, and downloads are written under downloads/ after purchase-style commands.] <br>

## Skill Version(s): <br>
1.0.22 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
