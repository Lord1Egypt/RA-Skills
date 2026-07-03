## Description: <br>
Scrapes posts from a Facebook group for a requested group URL, sort order, and count, returning structured JSON metadata for each visible post. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect structured post metadata from Facebook groups they can access through a logged-in browser session for monitoring, export, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can export personal information from Facebook group posts visible to the logged-in account. <br>
Mitigation: Run it only for groups and posts the user is authorized to access, avoid private or sensitive groups without permission, and review output before sharing or storing it. <br>
Risk: Bulk scraping through a logged-in browser session can trigger throttling, temporary account restrictions, or incomplete results. <br>
Mitigation: Use small counts, test with a minimal sample first, serialize requests, and add delays between group requests. <br>
Risk: Facebook session loss, access limits, or private-group permissions can produce empty or partial results. <br>
Mitigation: Verify login before execution, stop if the user cannot authenticate or lacks access, and do not use partial error responses as complete data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/facebook-groups-scrape-posts) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON returned through browser-act eval commands, with Markdown guidance for setup and execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in browser session and a Facebook group page visible to the user's account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
