## Description: <br>
Parses five-field cron expressions, generates Chinese human-readable descriptions, calculates upcoming run times, and lists common cron templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to interpret standard cron schedules in Chinese and check upcoming execution times before configuring or reviewing scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner guidance recommends review before installation when a skill requests broad access. <br>
Mitigation: Review the SKILL.md and bundled Python script before use; this artifact presents a local cron parsing CLI and no broad access request in the inspected files. <br>
Risk: Cron descriptions or next-run output may be misunderstood when used to configure scheduled jobs. <br>
Mitigation: Treat the output as review guidance and verify schedules against the target scheduler before deploying changes. <br>
Risk: Next-run calculations depend on an external Python package. <br>
Mitigation: Install croniter from a trusted package source and pin versions where reproducible scheduling review is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-cron-parser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3; next-run calculations require the croniter Python package.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
