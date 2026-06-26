## Description: <br>
Research Amazon products, track prices, and compare deals. Use when searching for products on Amazon, monitoring price changes, creating wishlists with price alerts, or comparing product specifications and reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcbuer](https://clawhub.ai/user/jcbuer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal shopping researchers use this skill to record Amazon product candidates, track manually entered or simulated prices, maintain wishlists, and compare deal information before purchasing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation may imply live Amazon price monitoring even though evidence indicates the code is local, manual, or simulated. <br>
Mitigation: Treat prices as advisory records and verify current Amazon listings before making purchase decisions. <br>
Risk: The setup script can add a recurring daily background task. <br>
Mitigation: Review the crontab entry before running setup, and install it only when recurring checks are intended. <br>
Risk: Product and price history can be retained in a local SQLite database. <br>
Mitigation: Store only product data you are comfortable retaining locally and remove the database when it is no longer needed. <br>


## Reference(s): <br>
- [Alu Profile Guide](references/alu_profile_guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jcbuer/amazon-research) <br>
- [Publisher Profile](https://clawhub.ai/user/jcbuer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite product and price records, and may install an optional daily cron task when the setup script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
