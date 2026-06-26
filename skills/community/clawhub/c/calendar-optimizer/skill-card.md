## Description: <br>
Analyzes and rewrites calendar events into clear, actionable tasks. Removes meeting fluff and converts vague descriptions into specific deliverables with deadlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to turn a calendar event and time into a clearer topic, actionability status, deadline signal, and preparation tip before deciding how to respond. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The usage documentation describes CSV input and Markdown output, but the artifact script accepts a single --event value and optional --time value. <br>
Mitigation: Use the actual script interface, --event and optionally --time, unless the author updates the artifact to support CSV input and Markdown output. <br>
Risk: Calendar text can contain sensitive meeting details even though the script does not access files, networks, credentials, or accounts. <br>
Mitigation: Try the skill locally with non-sensitive calendar text and review any output before sharing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1477009639zw-blip/calendar-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/1477009639zw-blip) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text terminal summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; the actual script accepts --event and optional --time.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
