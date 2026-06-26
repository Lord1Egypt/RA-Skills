## Description: <br>
Searches Bing or Baidu for Baidu Netdisk share links, verifies accessible resources, and helps save or transfer selected files into a user's Baidu Netdisk account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nameefef](https://clawhub.ai/user/nameefef) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find movies, shows, books, or other resources shared through Baidu Netdisk and transfer approved resources into their own netdisk storage. It is intended for workflows where the user can review the source link, extraction code, file details, and destination before any save or transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify a logged-in Baidu Netdisk account or authenticated bdpan CLI session. <br>
Mitigation: Require the agent to stop after finding links and ask for approval of the exact file, source link, and destination folder before any save or transfer. <br>
Risk: The skill searches third-party share links that may be expired, fake, misleading, or unsuitable. <br>
Mitigation: Verify link accessibility, file name, file size, and expiration before transfer, and search for alternatives when a link is invalid. <br>


## Reference(s): <br>
- [Browser Automation Patterns for Baidu Netdisk](references/browser-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nameefef/bdpan-resource-saver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with resource details and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Baidu Netdisk share links, extraction codes, file status, target folders, and transfer results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
