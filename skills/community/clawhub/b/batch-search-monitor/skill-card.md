## Description: <br>
Monitors batches of keywords on a schedule, alerts on search-result changes, and exports collected results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor keywords across Chinese search engines for competitor tracking, brand mention tracking, public-opinion alerts, market research, and data collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Keyword monitoring and result exports can include sensitive brand, competitor, or research terms. <br>
Mitigation: Review monitored keywords, notification settings, and export recipients before use, and avoid configuring confidential terms unless the operating environment is approved for them. <br>
Risk: The skill may use network access through curl to query supported search providers. <br>
Mitigation: Install and run it only in an environment with approved network egress, and review the skill contents and requested permissions before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaising-openclaw1/batch-search-monitor) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and CSV or Excel export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require curl and network access to supported search providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
