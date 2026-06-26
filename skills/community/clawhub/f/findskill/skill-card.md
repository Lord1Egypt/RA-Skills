## Description: <br>
Searches and discovers OpenClaw skills across multiple sources with bilingual Chinese and English query support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hgta23](https://clawhub.ai/user/hgta23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to find, inspect, filter, and compare available OpenClaw skills by keyword, tag, author, source, popularity, or related-skill recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search results may label mirror data as verified, which can mislead users about whether a skill is trustworthy. <br>
Mitigation: Confirm publisher, source, and provenance on ClawHub before installing or recommending a returned skill. <br>
Risk: Queries may be sent to external skill search sources, including an under-disclosed third-party mirror. <br>
Mitigation: Avoid confidential search terms and restrict use to approved environments and sources when discovery results influence installation decisions. <br>
Risk: The release evidence advises updating or pinning axios before deployment. <br>
Mitigation: Review dependency versions and pin or update axios according to the deployment environment's security policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hgta23/findskill) <br>
- [Publisher profile](https://clawhub.ai/user/hgta23) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text with skill summaries, source labels, scores, recommendations, details, and install commands when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call ClawHub, a third-party mirror, and GitHub APIs; search results may be cached locally during execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata, package.json, artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
