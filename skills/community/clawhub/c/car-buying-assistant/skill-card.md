## Description: <br>
Help Justin research, compare, and decide on new/used cars in Ontario, Canada and nearby markets using structured workflows, web research, and local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justintsmith](https://clawhub.ai/user/justintsmith) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to research car listings, compare candidates, identify red flags, and prepare negotiation drafts while keeping purchase decisions and seller contact under user control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent local car-shopping notes under ~/Documents/CarSearch/. <br>
Mitigation: Install only if that local storage behavior is acceptable, and review generated files for sensitive personal information. <br>
Risk: Seller message drafts could include inaccurate, incomplete, or sensitive information if sent without review. <br>
Mitigation: Review every draft before sending and avoid including payment details, SIN, banking information, credit-card numbers, or a full home address. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/justintsmith/car-buying-assistant) <br>
- [Publisher Profile](https://clawhub.ai/user/justintsmith) <br>
- [Report Template](artifact/scripts/report_template.md) <br>
- [Listing Normalizer](artifact/scripts/normalize_listings.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON listing data, negotiation drafts, and optional shell commands for local helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local car-search session files under ~/Documents/CarSearch/ when used as directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
