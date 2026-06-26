## Description: <br>
Adds a named book to a user's Douban Want to Read list by finding the best Douban Books result and running the authenticated two-step save flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinntrance](https://clawhub.ai/user/jinntrance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-assistant agents use this skill to add books to a Douban Want to Read list after the user has established a local Douban login session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill keeps a local Douban browser login profile that may preserve account access. <br>
Mitigation: Protect the profile directory and delete it to revoke stored access when the skill is no longer needed. <br>
Risk: Ambiguous book names may resolve to the first Douban search result rather than the intended title. <br>
Mitigation: Verify ambiguous titles before relying on the selected book result. <br>


## Reference(s): <br>
- [Douban Bookmark on ClawHub](https://clawhub.ai/jinntrance/douban-bookmark) <br>
- [jinntrance publisher profile](https://clawhub.ai/user/jinntrance) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON status output and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a headed browser login step and stores a local Douban browser profile for session reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
