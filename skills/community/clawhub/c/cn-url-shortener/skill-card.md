## Description: <br>
A Python URL-shortening skill that sends a user-provided URL to the public is.gd service and returns the resulting short link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents can use this skill to shorten public URLs for easier sharing. It is best suited for non-sensitive links because submitted URLs are sent to is.gd. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs are sent to the public is.gd service. <br>
Mitigation: Avoid using the skill for private internal URLs, login links, reset links, or URLs containing tokens or sensitive query parameters. <br>
Risk: The artifact documentation advertises statistics, expiry, and batch features that are incomplete or nonfunctional in this version. <br>
Mitigation: Rely on the implemented shortening behavior only, and verify any claimed advanced feature before depending on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-url-shortener) <br>
- [is.gd URL creation endpoint](https://is.gd/create.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [JSON response from the helper script and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to is.gd and a user-provided URL.] <br>

## Skill Version(s): <br>
1.2.5 (source: ClawHub release metadata; artifact SKILL.md declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
