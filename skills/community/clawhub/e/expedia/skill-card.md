## Description: <br>
Search Expedia stays, packages, cars, and activities, compare real trip costs, and run partner-safe booking workflows with web and API modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and compare Expedia stays, packages, cars, and activities, then prepare booking-safe summaries or authorized partner workflows. It is intended for Expedia-specific inventory, total-cost comparison, price-check, deeplink, and booking-preparation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trip search details may be sent to Expedia services during live lookups. <br>
Mitigation: Use live Expedia calls only when the user accepts sharing the relevant destination, date, traveler, and search context. <br>
Risk: Local travel-planning memory under ~/expedia/ can retain trip context. <br>
Mitigation: Keep saved notes minimal and redacted, and do not store API keys, shared secrets, payment details, or full authorization headers. <br>
Risk: Partner API workflows can involve credentials and authorization scope. <br>
Mitigation: Use partner credentials only for authorized Expedia integrations and clearly separate public web, redirect, and Rapid modes. <br>
Risk: Booking or payment steps can create financial or itinerary impact if final details are stale or incomplete. <br>
Mitigation: Require explicit approval after reviewing final price, fees, cancellation terms, traveler details, and authorization scope. <br>


## Reference(s): <br>
- [ClawHub Expedia Skill](https://clawhub.ai/ivangdavila/expedia) <br>
- [Expedia Skill Homepage](https://clawic.com/skills/expedia) <br>
- [Expedia Public Site](https://www.expedia.com/) <br>
- [Expedia Travel Redirect Listings Endpoint](https://apim.expedia.com/hotels/listings) <br>
- [Expedia Rapid API Endpoint](https://api.ean.com/v3/) <br>
- [Expedia Rapid Test API Endpoint](https://test.ean.com/v3/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Expedia mode labels, comparison tables, booking-safety status, redacted local memory notes, and authorized API request guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
