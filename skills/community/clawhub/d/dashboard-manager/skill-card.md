## Description:

Dashboard Manager reads, updates, and synchronizes a Jarvis dashboard data.json file in real time, including pending notes, logs, tasks, system status, statistics, and sub-agent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philippeh5](https://clawhub.ai/user/philippeh5)

### License/Terms of Use:

MIT

## Use Case:

Developers and Jarvis/OpenClaw users use this skill to keep a local Jarvis dashboard synchronized by reading pending notes and updating notes, logs, tasks, system status, heartbeat, token statistics, and sub-agent activity in data.json.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically modify the configured Jarvis dashboard data.json file.

Mitigation: Install only where that file should be modified, verify the configured path before use, and back up data.json before enabling automatic synchronization.

Risk: Data integrity issues can occur if data.json is missing, inaccessible, or invalid JSON.

Mitigation: Confirm file permissions and JSON validity during setup, and monitor the skill's logs for read or write failures.

Risk: The package declares fs and path dependencies even though those are Node.js built-in modules.

Mitigation: Remove the unnecessary dependency declarations before packaging or deployment to reduce install hygiene issues.

## Reference(s):

- [Dashboard Manager ClawHub page](https://clawhub.ai/philippeh5/skills/dashboard-manager)

## Skill Output:

**Output Type(s):** [code, configuration, text]

**Output Format:** [JavaScript module functions that read and write JSON data with text status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Modifies the configured local data.json file and returns parsed JSON data or boolean status values from helper functions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
