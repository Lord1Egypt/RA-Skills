## Description: <br>
Add governance to experiment workflows with PIN-protected destructive operations, standardized metric thresholds, compare-scores ranking with gating, and competition rules audit guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diamond2nv](https://clawhub.ai/user/diamond2nv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML engineers use this skill to add governance patterns to experiment workflows, including PIN checks for destructive actions, metric registries with thresholds, experiment ranking, and competition compliance audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destructive experiment actions can be performed without the intended PIN guard if automation normalizes `--force` or command-line PIN use. <br>
Mitigation: Require scoped automation permissions, audit logging, and human review for cancel, stop, delete, and PIN-clear workflows; avoid command-line PINs and treat `--force` as an exception path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diamond2nv/experiment-lifecycle-governance) <br>
- [expflow repository](https://github.com/diamond2nv/expflow) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides implementation patterns, CLI examples, metric threshold conventions, audit checks, and operational cautions for experiment governance.] <br>

## Skill Version(s): <br>
0.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
