## Description: <br>
Evaluate individual framework controls against organizational documentation with evidence extraction, severity classification, and remediation recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dangsllc](https://clawhub.ai/user/dangsllc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance, security, and audit practitioners use this skill to assess whether organizational documentation satisfies specific framework controls and to identify evidence-backed gaps with severity and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release evidence flags a suspicious security verdict because one bundled review helper may run a nested reviewer with unrestricted sandbox access. <br>
Mitigation: Install only if the publisher is trusted; before running autoreview, use `--no-yolo` or `AUTOREVIEW_YOLO=0` where appropriate and review fallback reviewer configuration. <br>
Risk: Review workflows can expose local diffs, including sensitive code or untracked files, to the configured reviewer. <br>
Mitigation: Review pending diffs before use and avoid running reviewer workflows on repositories containing sensitive uncommitted material. <br>


## Reference(s): <br>
- [Control Assessment on ClawHub](https://clawhub.ai/dangsllc/control-assessment) <br>
- [Rote Compliance Skills](https://github.com/Rote-Compliance/rote-compliance-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured JSON assessment, typically embedded in Markdown or returned as JSON when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes control identifiers, evidence quotes, coverage status, gap description, severity, recommendations, confidence, and reasoning.] <br>

## Skill Version(s): <br>
0.1.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
