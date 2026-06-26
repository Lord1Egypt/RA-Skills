## Description: <br>
Query Google Analytics 4 (GA4) data through the Google Analytics Data API for trends, countries, sources, pages, and conversion analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanaco666](https://clawhub.ai/user/nanaco666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to set up OAuth-based GA4 access and query reports such as active users, sessions, country/source breakdowns, page trends, and key-event analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup stores Google OAuth client and token files locally. <br>
Mitigation: Protect ~/.config/openclaw, keep the OAuth files private, and delete the token or revoke Google access when access is no longer needed. <br>
Risk: The installer edits the user's shell startup configuration. <br>
Mitigation: Review the installer before running it and confirm it only writes the intended GA4_PROPERTY_ID setting. <br>
Risk: Some setup instructions still reference the previous ga4-data-api path. <br>
Mitigation: Verify the installed skill path before copying or running commands. <br>


## Reference(s): <br>
- [GA4 Data API to OpenClaw setup](references/setup.md) <br>
- [ClawHub release page](https://clawhub.ai/nanaco666/ga4-connector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the query script returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only Google Analytics OAuth scope and local OAuth credential files.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
