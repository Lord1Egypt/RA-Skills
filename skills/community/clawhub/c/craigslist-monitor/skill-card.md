## Description: <br>
Scrapes Craigslist NY service ads to find small owner-operated businesses in Staten Island, Brooklyn, and Bronx for lead generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayJJimenez](https://clawhub.ai/user/JayJJimenez) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, marketing, and operations users use this skill to collect public Craigslist service-ad leads in selected New York City boroughs. It can print leads to the console or append a markdown lead table for outreach follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scrapes Craigslist and collects public contact details for outreach. <br>
Mitigation: Confirm the use complies with applicable site rules, outreach laws, and internal contact-data handling policies before running it. <br>
Risk: Saved lead files may contain phone numbers, listing URLs, and business-identifying details. <br>
Mitigation: Store saved lead files in an approved location, restrict access, and delete them when they are no longer needed. <br>
Risk: The optional weekly cron command creates recurring scraping activity. <br>
Mitigation: Install the cron job only when recurring collection is intended, and review or remove the schedule when the campaign ends. <br>
Risk: The script depends on a local Scrapling environment. <br>
Mitigation: Verify the local Scrapling dependency and path before execution so the skill runs in the expected environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JayJJimenez/craigslist-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/JayJJimenez) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact monitor script](artifact/monitor.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, guidance] <br>
**Output Format:** [Console text and markdown tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can append lead results to a local markdown file and optionally enrich listings by fetching individual ad pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
