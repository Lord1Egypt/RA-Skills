## Description: <br>
Check for co-authorship conflicts between authors and suggested reviewers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Editors, journal staff, and research workflow operators use this skill to compare submitted authors with suggested reviewers and flag potential co-authorship conflicts before peer review assignments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that an autoreview helper can default to broad full-access agent execution and may share local diffs with fallback reviewers. <br>
Mitigation: Review the helper before installation or invocation, run it with --no-yolo or AUTOREVIEW_YOLO=0, and disable automatic fallback reviewers for sensitive repositories. <br>
Risk: Local diffs or input files may contain sensitive information. <br>
Mitigation: Avoid running the skill where sensitive local changes or private review data are present, and restrict use of moderation commands to authorized staff with explicit targets and reasons. <br>


## Reference(s): <br>
- [Conflict Of Interest Checker on ClawHub](https://clawhub.ai/AIPOCH-AI/conflict-of-interest-checker) <br>
- [AIPOCH-AI publisher profile](https://clawhub.ai/user/AIPOCH-AI) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text report with conflict findings and reviewer recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts comma-separated authors and reviewers, with an optional CSV publication file.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
