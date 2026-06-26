## Description: <br>
Query eBusy-based tennis hall bookings via a small Python client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogruenig](https://clawhub.ai/user/ogruenig) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to log into a configured eBusy tennis booking site, fetch reservations for a selected court module and date, and present booking information or availability summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires eBusy login credentials for the selected hall. <br>
Mitigation: Provide credentials only through the runtime environment or local secret management, and do not publish secret-bearing files with the skill. <br>
Risk: A misconfigured EBUSY_BASE_URL could send credentials or booking requests to the wrong site. <br>
Mitigation: Verify EBUSY_BASE_URL points to the intended club site before running the client. <br>
Risk: Returned reservation names or notes may contain private booking information. <br>
Mitigation: Treat reservation output as private and limit sharing to the intended user or authorized workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ogruenig/ebusy-courts) <br>
- [Medenhalle Wiesbaden-Medenbach eBusy example](https://medenhalle.ebusy.de) <br>
- [KTEV Kelkheim eBusy example](https://ktev.ebusy.de) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text reservation lines and Markdown setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires eBusy base URL, credentials, court module ID, and date configuration from the runtime environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
