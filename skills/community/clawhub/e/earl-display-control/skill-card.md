## Description:

Manage Earl's TV dashboard (VisuoSpatial Sketchpad): wake the display, restart the local server, launch a kiosk browser, and update Earl's mind state for mood, household tasks, hot takes, doodles, and weather.

This skill is ready for commercial/non-commercial use.

## Publisher:

[recozers](https://clawhub.ai/user/recozers)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate a local living-room dashboard: start or recover the server and kiosk browser, update household display content through the included Python API, and maintain the earl_mind.json state file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard state can contain household reminders, room notes, patterns, and optional precise coordinates.

Mitigation: Install only when that local data exposure is acceptable; use approximate coordinates or disable weather when location privacy matters.

Risk: A local HTTP server on port 8000 could expose dashboard state if reachable by other devices.

Mitigation: Bind the server to 127.0.0.1 and avoid exposing port 8000 beyond the local machine.

Risk: Untrusted messages or web content could affect displayed state if allowed to write into earl_mind.json.

Mitigation: Do not allow untrusted inputs to write to the state file until rendered fields are escaped or sanitized.

Risk: Clear/reset helpers and force-kill commands can remove state or terminate the wrong process.

Mitigation: Back up earl_mind.json before destructive updates and verify the target process before running force-kill commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/recozers/skills/earl-display-control)
- [Project homepage](https://github.com/recozers/earl-display-control)
- [Open-Meteo forecast API](https://api.open-meteo.com/v1/forecast)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and JSON configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update a local JSON state file and provide browser/server commands for a local dashboard.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
