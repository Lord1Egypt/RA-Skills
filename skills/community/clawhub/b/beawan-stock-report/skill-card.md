## Description: <br>
Helps agents query Beawan for A-share listed company financial report analysis URLs, including first-quarter, interim, third-quarter, and annual reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sqjsytqte](https://clawhub.ai/user/sqjsytqte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Beawan analysis pages for A-share listed company financial reports by stock code, year, and report type. The skill requires a Beawan API key before requests can be made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented Beawan endpoint uses unencrypted HTTP while requiring an API key. <br>
Mitigation: Do not send production credentials to the documented HTTP endpoint; use only test credentials or wait for HTTPS-only service guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sqjsytqte/beawan-stock-report) <br>
- [Beawan report lookup API](http://api.beawan.com/beawanSkill/api/skill/report) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, Text] <br>
**Output Format:** [Markdown instructions with HTTP request examples and a JSON response shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a report analysis URL when the Beawan API request succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
