## Description: <br>
Queries OneHai through the user's logged-in macOS Chrome session to return China domestic rental-car reference prices, booking URLs, selected store details, and policy restrictions that may look like zero inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tengjiaozhai](https://clawhub.ai/user/tengjiaozhai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel-planning users and agents use this skill to check China domestic self-drive rental reference prices from OneHai, especially for same-day or holiday trips where train-station or airport store choice matters. It helps distinguish true no-inventory results from peak-period minimum-rental restrictions. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a logged-in Chrome session and runs JavaScript in that browser context. <br>
Mitigation: Use a dedicated Chrome profile logged into only OneHai, and disable Chrome Apple Events JavaScript after running the query. <br>
Risk: The skill opens Chrome tabs and processes page content locally with tesseract. <br>
Mitigation: Run it only in an environment where local browser automation and local page-content processing are acceptable. <br>
Risk: Returned prices are reference prices captured at query time, not guaranteed checkout totals. <br>
Mitigation: Present results as reference real-time prices and verify final terms on the OneHai booking page before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tengjiaozhai/china-rental-price) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tengjiaozhai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the query script plus a concise natural-language summary for the user] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reference prices are captured at query time and are not guaranteed final checkout prices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
