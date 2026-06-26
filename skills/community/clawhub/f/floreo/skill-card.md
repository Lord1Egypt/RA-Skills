## Description: <br>
Floreo is an autonomous compounding journal for local-first life logging, activity detection, compound metrics, cross-domain correlations, and optional external service sync with privacy controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coidea](https://clawhub.ai/user/coidea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Floreo to structure personal journaling, health and productivity tracking, imports, privacy-screened exports, and optional automated analysis across local files and connected services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous monitoring can observe sensitive folders, repositories, calendars, or services beyond the user's intended scope. <br>
Mitigation: Confirm exactly which locations and services are watched before enabling automation, and keep watchers or cron jobs disabled unless they are needed. <br>
Risk: Broad local imports and life-log entries can collect sensitive personal, health, work, or relationship data. <br>
Mitigation: Preview bulk imports, use privacy tiers deliberately, and review entries before exporting or syncing them. <br>
Risk: Optional external sync can expose private journal data or service credentials. <br>
Mitigation: Leave external sync off by default, use least-privilege API keys, store tokens securely, and document how to revoke tokens and remove synced data. <br>
Risk: Scheduled automation may persist after the user stops actively using the skill. <br>
Mitigation: Maintain a clear disable path for cron jobs, file watchers, stored tokens, and imported data. <br>


## Reference(s): <br>
- [Floreo ClawHub listing](https://clawhub.ai/coidea/floreo) <br>
- [Floreo project homepage](https://github.com/openclaw/floreo) <br>
- [Release notes v0.2.0](RELEASE_v0.2.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file-path conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local journal entries, reports, exports, and optional sync/setup instructions.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence, clawhub.json, _meta.json, and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
