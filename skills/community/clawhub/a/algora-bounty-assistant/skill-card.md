## Description: <br>
Automatically search for low-competition GitHub bounty tasks and generate a concise report with issue details and estimated difficulty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[santosparra651-arch](https://clawhub.ai/user/santosparra651-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and bounty hunters use this skill to find open GitHub issues labeled as bounties with lower comment counts, then review a report that helps prioritize opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub issue titles and descriptions are untrusted third-party content. <br>
Mitigation: Review bounty details manually before acting on generated reports or recommendations. <br>
Risk: Publisher provenance is minimal because no server-resolved GitHub import provenance is stored for this version. <br>
Mitigation: Review the artifact and publisher profile before using the skill in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/santosparra651-arch/algora-bounty-assistant) <br>
- [GitHub Search API endpoint](https://api.github.com/search/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports public GitHub issue titles, URLs, comment counts, and simple difficulty or value heuristics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
