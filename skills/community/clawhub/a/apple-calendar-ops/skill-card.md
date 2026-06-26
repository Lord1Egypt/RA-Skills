## Description: <br>
Reads, creates, updates, and deletes Apple Calendar events via CalDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ivy-End](https://clawhub.ai/user/Ivy-End) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and scheduler/orchestrator systems use this skill to inspect Apple Calendar data and perform explicit calendar create, update, and delete operations through a stable CalDAV interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stored Apple Calendar credentials can authorize real calendar reads, writes, updates, and deletes. <br>
Mitigation: Install only when that authority is acceptable, prefer a dedicated app-specific password, and verify baseUrl, calendarUrls, and timezone before use. <br>
Risk: Update and delete targets are not strictly constrained to known calendars. <br>
Mitigation: Use dry-run before writes and pass only event IDs returned by this skill's fetch output until target URL allowlisting is enforced. <br>


## Reference(s): <br>
- [Apple Calendar Ops Boundary](references/boundary.md) <br>
- [Normalized Event Contract](references/event-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, shell commands, configuration] <br>
**Output Format:** [JSON responses from CLI scripts, with markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calendar operations use Apple Calendar credentials from secrets.json and support dry-run behavior for write previews where practical.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
