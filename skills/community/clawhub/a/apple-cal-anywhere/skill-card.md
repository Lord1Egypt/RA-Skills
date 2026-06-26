## Description: <br>
Apple Cal Anywhere lets an agent manage iCloud Calendar over CalDAV, including event CRUD, multi-calendar queries, managed attachments, and free/busy lookups on macOS, Linux, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xushen-ma](https://clawhub.ai/user/xushen-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect an agent to iCloud Calendar so it can list, create, update, and delete events, manage attachments, and check availability after the user provides iCloud credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change iCloud Calendar data when credentials are provided. <br>
Mitigation: Install it only for intended calendar-management use and review create, update, delete, and attach commands before running them. <br>
Risk: The Apple app-specific password could be exposed if stored in shared shell profiles or logs. <br>
Mitigation: Use an Apple app-specific password and prefer a private environment or keyring storage for APPLECAL_PASSWORD. <br>
Risk: Attachment commands can upload local files to calendar events. <br>
Mitigation: Use APPLECAL_ATTACH_DIR to limit uploads to a safe folder and rely on the skill's extension and sensitive-path checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xushen-ma/apple-cal-anywhere) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>
- [Apple app-specific password portal](https://appleid.apple.com) <br>
- [RFC 4791 CalDAV](https://www.rfc-editor.org/rfc/rfc4791) <br>
- [RFC 8607 Calendar Managed Attachments](https://www.rfc-editor.org/rfc/rfc8607) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with bash examples; CLI commands return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, an iCloud account with Calendar enabled, and APPLECAL_PASSWORD or a supported keyring credential.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and scripts/applecal.py __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
