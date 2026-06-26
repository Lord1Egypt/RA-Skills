## Description: <br>
Collects Booking hotel information through the Dataify Scraper API by creating Dataify Booking URL collection tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare and confirm Booking URL scraping parameters, handle a Dataify API token, submit a Dataify collection task, and report the resulting task status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a persistent Dataify API token and may receive user-supplied Booking URLs or scraping inputs. <br>
Mitigation: Use a dedicated Dataify token where possible, do not paste or log the token, and confirm parameters before any API call. <br>
Risk: Submitted scraping jobs are processed by Dataify. <br>
Mitigation: Do not submit private URLs, account data, cookies, or other sensitive inputs unless the user intends Dataify to process them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-booking-hotellist) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown confirmation tables, text status summaries, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Dataify collection tasks after user confirmation and token handling.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
