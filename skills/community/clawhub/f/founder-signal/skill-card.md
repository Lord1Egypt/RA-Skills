## Description: <br>
Founder Signal turns verified Reddit and V2EX evidence into a small, reviewable signal package for founders evaluating product demand and positioning across one or more configured product profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[toliuweijing](https://clawhub.ai/user/toliuweijing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Founders and product teams use this skill to gather verified Reddit and V2EX demand signals, score candidate evidence, and generate reviewable founder research artifacts for product positioning decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Every run review is automatically sent to a public Draft page by default, including failed or no-evidence runs. <br>
Mitigation: Use only public-safe product profiles and evidence snapshots, or modify the workflow to require explicit approval before any Draft publication. <br>
Risk: The documented config confirmation flag is not a reliable gate for Draft publication in this version. <br>
Mitigation: Review generated public-run-review.md and draft-publish-intent.json before running with sensitive internal research, and disable or gate the automatic Draft publish step when privacy matters. <br>


## Reference(s): <br>
- [Founder Signal ClawHub page](https://clawhub.ai/toliuweijing/founder-signal) <br>
- [Draft CLI dependency](https://clawhub.ai/toliuweijing/draft-cli) <br>
- [Profile setup documentation](profiles/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON run artifacts, Draft publish intent JSON, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local run folders under the Founder Signal runtime home and prepares a Draft public-page publish intent for each profile run.] <br>

## Skill Version(s): <br>
0.2.14 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
