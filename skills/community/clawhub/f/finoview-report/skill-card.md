## Description: <br>
Calls the Finoview futures research report API to retrieve weekly futures reports by date or category, including titles, authors, summaries, and PDF links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finoview](https://clawhub.ai/user/finoview) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to fetch Finoview futures weekly research reports for market analysis, report aggregation, and market intelligence collection. It requires Finoview API credentials before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guide includes a verification snippet that can print FINOVIEW_API_SECRET and expose credentials. <br>
Mitigation: Do not print secrets; verify credential presence with masked output or a presence-only check. <br>
Risk: The skill requires sensitive Finoview API credentials to fetch reports. <br>
Mitigation: Use the skill only if you trust it with those credentials, prefer temporary environment variables or a secret manager, and rotate credentials when appropriate. <br>


## Reference(s): <br>
- [Finoview API host](https://www.finoview.com.cn) <br>
- [ClawHub skill listing](https://clawhub.ai/finoview/finoview-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [JSON data and Markdown report summaries or tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINOVIEW_API_KEY and FINOVIEW_API_SECRET; API results include report metadata, summaries, and PDF links.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
