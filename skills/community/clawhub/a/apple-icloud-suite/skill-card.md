## Description: <br>
Apple iCloud Suite helps agents work with iCloud calendars, photos, iCloud Drive, Find My devices, and reminders through documented command-line workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovensky1992-wk](https://clawhub.ai/user/lovensky1992-wk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect and manage Apple iCloud calendars, photos, files, device location, and reminders. It is also used for household coordination workflows that publish status or schedule information to shared calendars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require broad iCloud account credentials and cached sessions. <br>
Mitigation: Avoid pasting a primary Apple ID password into chat, prefer app-specific credentials where supported, and review or clear local iCloud session files after use. <br>
Risk: The status-wall workflow can continuously track and publish personal location or schedule status. <br>
Mitigation: Keep the daemon disabled unless deliberately needed and confirm every tracked person has consented. <br>
Risk: Precise location data may be sent to AMap for reverse geocoding. <br>
Mitigation: Use the AMap integration only with informed consent and avoid it when precise location sharing is not acceptable. <br>
Risk: Shared-calendar publishing can expose private schedule or location-derived status. <br>
Mitigation: Limit shared-calendar access and review generated events before sharing them with household or team members. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lovensky1992-wk/apple-icloud-suite) <br>
- [Calendar reference](references/calendar.md) <br>
- [Photos reference](references/photos.md) <br>
- [Find My reference](references/findmy.md) <br>
- [iCloud Drive reference](references/drive.md) <br>
- [Script reference](references/scripts.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to read service-specific reference files before proposing iCloud actions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
