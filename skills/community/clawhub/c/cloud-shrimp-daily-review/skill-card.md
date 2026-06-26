## Description: <br>
Daily Review Assistant helps agents manually trigger daily reviews, query historical review records, generate review statistics, and export review content across time ranges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pagoda111king](https://clawhub.ai/user/pagoda111king) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals or teams using the Daily Review System use this skill to run on-demand reviews, retrieve prior review notes, create summary statistics, and export review content without waiting for the scheduled 23:00 Cron review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported daily review records may contain sensitive conversation summaries, plans, work context, or personal reflections. <br>
Mitigation: Review exported files before sharing them and restrict where review records are stored or transmitted. <br>
Risk: The package contains placeholder executable code and appears to rely on a separate Daily Review System or Cron job for real review behavior. <br>
Mitigation: Confirm the separate review system exists in the target environment and test manual review, query, statistics, and export flows before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pagoda111king/cloud-shrimp-daily-review) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Artifact package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review reports, summary statistics, exported review content, and agent-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference daily review records saved under memory/evolution/daily-review/ when the separate daily review system is present.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
