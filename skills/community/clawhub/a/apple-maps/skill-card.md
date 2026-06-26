## Description: <br>
Search places, open routes, and run Apple Maps workflows on macOS using local CLI commands and shortcut automation with explicit safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill on macOS to search places, open Apple Maps routes, generate reusable map links, and manage local Apple Maps workflow preferences with confirmation gates for sharing and bulk actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Place searches, route origins and destinations, and map parameters may be sent to Apple Maps. <br>
Mitigation: Use minimal query strings, preview generated URLs, and avoid sending sensitive location context unless the user confirms. <br>
Risk: Opening multiple map links or sharing generated links can expose private context or disrupt the user's workspace. <br>
Mitigation: Default to one link at a time, show counts for bulk actions, and require explicit confirmation before bulk opens or external sharing. <br>
Risk: Fallback automation through shortcuts or osascript may be less deterministic than direct Apple Maps URL launches. <br>
Mitigation: Prefer open -a Maps with explicit URLs, probe command availability first, and explain capability limits before using fallback paths. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ivangdavila/apple-maps) <br>
- [Skill homepage](https://clawic.com/skills/apple-maps) <br>
- [Apple Maps endpoint](https://maps.apple.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Apple Maps URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local configuration files under ~/apple-maps/ only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
