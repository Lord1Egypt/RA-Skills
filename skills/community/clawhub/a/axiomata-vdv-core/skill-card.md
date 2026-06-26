## Description: <br>
VDV Core (Vision de Verite / Truth Vision) is a universal protocol for analyzing complex or contradictory information by mapping tensions, locating invariant points, and optionally validating phi alignment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to structure truth-seeking analysis of dense, contradictory, or high-entropy information and to produce a VDV analysis with trigger, silence, tension, attractor, and reinforcement sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts can read user-specified local files and store derived analysis in local JSON files. <br>
Mitigation: Avoid using the file input or storage options with secrets, personal data, or private documents unless retaining derived results locally is intended. <br>
Risk: The skill produces heuristic text analysis that may be incomplete or misleading for high-stakes decisions. <br>
Mitigation: Treat outputs as analysis aids and have a qualified human review conclusions before operational, legal, medical, financial, or safety-sensitive use. <br>
Risk: Running local Python helper scripts executes code from the artifact in the user's environment. <br>
Mitigation: Review the scripts and run them only in an environment where local file access and JSON output creation are acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON outputs from local Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Optional local JSON storage keeps up to the last 100 stored results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
