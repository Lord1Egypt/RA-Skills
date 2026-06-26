## Description: <br>
Monitor overall App Store ratings for configured iOS apps across multiple countries using Apple's free iTunes Lookup API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aligurelli](https://clawhub.ai/user/aligurelli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product teams, and app operators use this skill to fetch current overall App Store ratings for selected iOS apps across configured countries, either on demand or through a daily report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A daily cron setup can create recurring messages that continue after they are no longer wanted. <br>
Mitigation: Confirm the schedule before enabling it and keep track of where the cron job is configured so it can be disabled. <br>
Risk: Incorrect or untrusted app IDs and country codes can produce misleading N/A results or unexpected API queries. <br>
Mitigation: Use only trusted App Store IDs and ISO country codes in the APPS array, and review all-N/A output or script errors before acting on the report. <br>
Risk: The script relies on local bash, curl, and python3 plus Apple's public lookup endpoint, so local tooling or network failures can affect the report. <br>
Mitigation: Run it with trusted local tools and treat errors or missing API responses as a signal to retry or verify ratings through another source. <br>


## Reference(s): <br>
- [Apple iTunes Lookup API endpoint](https://itunes.apple.com/lookup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text rating report with shell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ratings use a comma decimal separator, and unavailable ratings are reported as N/A.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
