## Description: <br>
Google Calendar via gcalcli: today-only agenda by default, bounded meaning-first lookup via agenda scans, and fast create/delete with verification--optimized for low tool calls and minimal output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mbright4497](https://clawhub.ai/user/mbright4497) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal-assistant operators use this skill to let an agent read, search, create, and delete Google Calendar events through gcalcli after local OAuth setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can read calendar events across non-ignored calendars using the user's existing gcalcli Google Calendar permissions. <br>
Mitigation: Install only where those gcalcli permissions are acceptable and rely on gcalcli's existing local OAuth setup. <br>
Risk: Unambiguous delete or edit requests may be executed without an additional confirmation prompt. <br>
Mitigation: For a more conservative workflow, edit the skill to require confirmation before every delete or edit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mbright4497/gcalcli-calendar-3-0-0) <br>
- [gcalcli project](https://github.com/insanum/gcalcli) <br>
- [Google Calendar API endpoint](https://www.googleapis.com/calendar/) <br>
- [Google OAuth2 token endpoint](https://oauth2.googleapis.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed and authenticated gcalcli binary; no skill-managed credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json reports 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
