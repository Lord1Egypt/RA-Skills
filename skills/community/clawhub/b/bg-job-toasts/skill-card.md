## Description: <br>
Background Job Toasts guides implementation and troubleshooting of bottom-right background job status toasts, cron job name enrichment, and compaction progress feedback in the OpenClaw Control UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers working on OpenClaw use this skill to add, improve, or troubleshoot UI visibility for cron jobs, memory compaction, knowledge extraction, and other background processes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron job names may be displayed in UI toast messages, which can expose sensitive labels if sensitive information is used in job names. <br>
Mitigation: Use non-sensitive cron job names and review generated changes that broadcast or render cron payload names. <br>
Risk: Background job status can appear stale or misleading if UI state mutations do not trigger a render. <br>
Mitigation: Review generated UI changes for explicit render updates where the artifact notes state is not reactive. <br>


## Reference(s): <br>
- [Source Snapshot](references/source-snapshot.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/bg-job-toasts) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with TypeScript and CSS snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Implementation guidance should be reviewed before applying generated UI state or broadcast changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
