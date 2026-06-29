## Description: <br>
Amazon Seller Central SP-API wrapper (Python) for orders, catalog, FBA inventory, reports, restock recommendations, and financial events, with SigV4 and LWA refresh handled internally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[berkgungor](https://clawhub.ai/user/berkgungor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can use this skill to query Amazon Seller Central data through SP-API for order review, inventory checks, report generation, restock planning, and financial reconciliation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Amazon Seller Central data through SP-API credentials. <br>
Mitigation: Use least-privilege Amazon and IAM credentials and install it only for environments where that access is intended. <br>
Risk: Required tokens and client secrets could be exposed if pasted into chat or written into shared files. <br>
Mitigation: Store credentials in a shell environment or secrets manager and keep secrets out of chat. <br>
Risk: Report commands can write downloaded Seller Central data to local paths. <br>
Mitigation: Write reports only to deliberate, non-sensitive locations and review files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/berkgungor/skills/amazon-sp-api) <br>
- [Amazon Selling Partner API documentation](https://developer-docs.amazon.com/sp-api/) <br>
- [Amazon SP-API marketplace IDs](https://developer-docs.amazon.com/sp-api/docs/marketplace-ids) <br>
- [Amazon SP-API report type values](https://developer-docs.amazon.com/sp-api/docs/report-type-values) <br>
- [HTTPX documentation](https://www.python-httpx.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; bundled script output is JSON, with optional TSV files for downloaded reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Amazon SP-API and AWS credential environment variables; report commands may write files when an output path is supplied.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
