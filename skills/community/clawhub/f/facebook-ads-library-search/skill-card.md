## Description: <br>
Searches Meta Ad Library by keyword or Facebook page ID and returns structured ad details including creatives, copy, calls to action, publisher platforms, spend, impressions, reach estimates, and page transparency information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to collect structured Meta Ad Library results for ad transparency, competitor research, brand monitoring, and political or housing ad review from data visible in their browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs automated Meta Ad Library collection through browser-context Facebook requests, which may create compliance or rate-limit risk if used at high volume. <br>
Mitigation: Install only when this collection is intended, keep request volumes conservative, and review generated commands or scripts before running them. <br>
Risk: The security summary flags under-disclosed backend Facebook automation, page-token use, local persistence, and stealth scaling guidance. <br>
Mitigation: Avoid stealth multi-session scaling guidance, monitor or delete local memory and output files if they are created, and review browser-context behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/facebook-ads-library-search) <br>
- [Facebook prerequisite page](https://www.facebook.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell command templates and JSON result objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paginated results include count, has_next_page, end_cursor, and ads fields; some ad metrics may be null depending on Meta availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
