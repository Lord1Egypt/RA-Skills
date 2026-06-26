## Description: <br>
Review code for correctness, security, performance, and maintainability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to review code snippets, files, or diffs before merging, investigating suspected bugs, or performing security hardening. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Code or diffs submitted for review may contain sensitive information. <br>
Mitigation: Only provide code you are comfortable sharing with the agent runtime and follow local data handling rules. <br>
Risk: Malformed trigger metadata may cause the skill to activate outside intended review requests. <br>
Mitigation: The publisher should correct the trigger metadata, and users should invoke the skill only for explicit review tasks. <br>
Risk: Review recommendations may be incomplete or incorrect. <br>
Mitigation: Validate findings against the referenced code, tests, and project constraints before making changes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown review report with prioritized findings and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to include evidence and distinguish must-fix issues from nice-to-have improvements.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
