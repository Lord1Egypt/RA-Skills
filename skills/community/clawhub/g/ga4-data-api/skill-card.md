## Description: <br>
Query Google Analytics 4 (GA4) data through the Google Analytics Data API for trends, countries, sources, pages, and conversion analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nanaco666](https://clawhub.ai/user/nanaco666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to set up OAuth user authorization for GA4 and query GA4 metrics inside OpenClaw. It helps inspect trends, country and source breakdowns, page activity, and conversion or key-event data while checking account permissions first. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup stores Google Analytics OAuth client and token files under ~/.config/openclaw. <br>
Mitigation: Treat ga4-client.json and ga4-token.json as sensitive, avoid shared machines, and delete the files or revoke the OAuth grant when access is no longer needed. <br>
Risk: The installer edits the user's shell startup configuration to set GA4_PROPERTY_ID. <br>
Mitigation: Review the ~/.bashrc or ~/.zshrc change after installation and remove the exported property ID when it is no longer required. <br>


## Reference(s): <br>
- [GA4 Data API setup](references/setup.md) <br>
- [ClawHub release page](https://clawhub.ai/nanaco666/ga4-data-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON query output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local OAuth client and token files for read-only Google Analytics API access.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
