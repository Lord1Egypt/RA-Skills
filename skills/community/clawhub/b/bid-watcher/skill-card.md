## Description: <br>
Bid Watcher monitors lithium battery, energy storage, and assembly-line bid opportunities, tracks four competitor companies, generates weekly reports, and can send reports by email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardcoder849](https://clawhub.ai/user/richardcoder849) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, market intelligence, and business development teams use this skill to collect bid leads in the lithium battery and energy storage equipment market, enrich them with company and priority context, and generate weekly follow-up reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill weakens HTTPS security while collecting bid data. <br>
Mitigation: Restore normal HTTPS certificate verification before scheduled runs or production use. <br>
Risk: Generated reports may contain sensitive bid intelligence and can be emailed through configured SMTP credentials. <br>
Mitigation: Treat generated reports as sensitive business information, use a dedicated SMTP app password, and restrict recipient lists. <br>
Risk: Scraped bid data and priority scores may be incomplete, stale, or require business review before action. <br>
Mitigation: Review source links, extracted fields, and priority scores before using the report for sales or procurement decisions. <br>


## Reference(s): <br>
- [ClawHub Bid Watcher release page](https://clawhub.ai/richardcoder849/bid-watcher) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/richardcoder849) <br>
- [Bid Watcher skill definition](artifact/SKILL.md) <br>
- [Search source configuration](artifact/scripts/search_bids.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands] <br>
**Output Format:** [JSON data files, Markdown reports, Excel workbooks, email status text, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are stored locally under data/ and may be sent through configured SMTP credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
