## Description: <br>
Runs a structured adversarial multi-agent review loop for significant documents, collecting reviewer redlines and guiding the user toward an explicitly reasoned revised version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scott3j](https://clawhub.ai/user/scott3j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and product teams use this skill to stress-test substantial documents before implementation or publication. It helps organize reviewer personas, collect redlines, record agree/disagree/modify positions, and produce a revised Markdown document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed documents are copied into ~/.openclaw/workspace/reviews/ and may be sent to spawned reviewer model sessions. <br>
Mitigation: Use the skill only with documents appropriate for those storage and model-review paths, and delete old review folders when they are no longer needed. <br>
Risk: The copy helper can run shell commands from a destination path because it expands the destination with eval. <br>
Mitigation: Before running scripts/cp-output.sh, remove the eval-based path expansion or avoid any destination value containing shell syntax such as command substitutions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scott3j/adversarial-review) <br>
- [Redline Format Specification](references/redline-format.md) <br>
- [Review Type Bundles](references/review-types.md) <br>
- [Reviewer Personas](references/reviewer-personas.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown redlines, position logs, revised document files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local review session folders under ~/.openclaw/workspace/reviews/ when its helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
