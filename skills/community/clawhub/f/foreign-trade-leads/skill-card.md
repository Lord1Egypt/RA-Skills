## Description: <br>
Collects B2B foreign-trade leads from Google Maps for overseas distributors, wholesalers, buyers, and local businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingfan0828](https://clawhub.ai/user/xingfan0828) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and sales teams use this skill to collect overseas B2B leads by confirming a product keyword, target region, and count, then running the bundled Google Maps scraper to save results as CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps scraping may be rate-limited, blocked, or restricted by platform-use terms. <br>
Mitigation: Confirm platform-use requirements before running the scraper and keep target counts moderate. <br>
Risk: Generated CSV files may contain identifiable business contact information. <br>
Mitigation: Store and share CSV outputs according to applicable privacy, legal, and compliance requirements. <br>
Risk: The scraper requires a local Selenium and Chrome driver environment. <br>
Mitigation: Verify Chrome and driver availability before use, and stop if the environment cannot run the bundled script. <br>


## Reference(s): <br>
- [Foreign Trade Leads release page](https://clawhub.ai/xingfan0828/foreign-trade-leads) <br>
- [Publisher profile](https://clawhub.ai/user/xingfan0828) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and CSV file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script writes a local CSV containing name, phone, address, website, and email columns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
