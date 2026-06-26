## Description: <br>
Monitor websites for changes, new content, and price alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t3mr0i](https://clawhub.ai/user/t3mr0i) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Businesses and individuals use this skill to monitor public websites for changed content, new listings, job postings, product prices, and other updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring checks can create unwanted load or violate site policies if targets and intervals are not chosen carefully. <br>
Mitigation: Configure only specific public URLs with clear monitoring goals, use conservative polling intervals, and avoid sites whose policies prohibit automated fetching. <br>
Risk: Monitoring private or authenticated pages can expose sensitive targets or collect information the user should not automate. <br>
Mitigation: Do not use the skill on private or authenticated pages, and review scheduled checks regularly so they can be stopped easily. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration] <br>
**Output Format:** [Command-line text output and local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configured URLs and stored page hashes to report detected changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
