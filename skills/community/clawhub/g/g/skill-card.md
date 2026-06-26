## Description: <br>
Google全家桶入口 is a ClawHub skill that lists 20+ Google and YouTube services by category and opens the selected official HTTPS page. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users use this skill as a compact launcher for Google search, communication, productivity, maps, media, and utility services. It helps users find a listed product, read a short description, and open the corresponding official page. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad trigger name "g" may be invoked when the user intended a different action. <br>
Mitigation: Use explicit invocation and confirm the selected Google product before opening a page. <br>
Risk: Opening links in the default browser may use the user's existing authenticated browser session. <br>
Mitigation: Review the destination URL before interacting with the opened Google or YouTube service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/g) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, browser navigation] <br>
**Output Format:** [Console text listing product categories, names, descriptions, and official HTTPS URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open the selected URL in the user's default browser.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
