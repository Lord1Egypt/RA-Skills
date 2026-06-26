## Description: <br>
Searches Bilibili with Playwright, selects a matching video result, and opens it in the user's macOS browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[e421083458](https://clawhub.ai/user/e421083458) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to search Bilibili for requested videos, music, documentaries, tutorials, or other media and open a matching result in the local browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Bilibili and opened pages may be associated with the user's normal browser session. <br>
Mitigation: Use a separate browser profile or log out before use when searches or playback should not be tied to an existing account. <br>
Risk: The skill opens external video or search pages selected from Bilibili results. <br>
Mitigation: Review the opened page before interacting with it or relying on its contents. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Command-line output and browser-opened Bilibili page] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, Playwright, macOS open command, and network access to Bilibili.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
