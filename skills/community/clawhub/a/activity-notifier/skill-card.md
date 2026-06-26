## Description: <br>
Broadcast agent activity status to a Discord channel for transparency while an agent is thinking, using tools, searching the web, coding, finishing, or reporting errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silvermoonswk](https://clawhub.ai/user/silvermoonswk) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to send concise progress updates to a configured Discord channel during long-running or multi-step agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord activity updates can reveal task context to people with access to the configured channel. <br>
Mitigation: Verify the channel audience, keep updates high-level, and avoid secrets, confidential filenames, private URLs, and sensitive incident details. <br>
Risk: Frequent status notifications can create distracting channel noise. <br>
Mitigation: Send updates only for meaningful progress on longer tasks and keep each message concise. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Concise Discord status messages, often as Markdown-formatted text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Discord token configuration and a target channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
