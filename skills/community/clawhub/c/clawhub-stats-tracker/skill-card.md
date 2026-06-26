## Description: <br>
Clawhub Stats Tracker helps an agent view published ClawHub skill operating metrics, including stars, downloads, installs, versions, and publication times. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub skill publishers use this skill to check operational metrics for tracked skills, inspect individual skill stats, or compare related skill series. It is intended for read-only stats review, not publishing, installation, deletion, or search workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub stats tracking issue](https://github.com/openclaw/clawhub/issues/156) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, JSON examples, and tabular stats output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Security posture from clawscan: suspicious. Install only if the user trusts and controls ~/.clawhub/tracked-skills.json, review or patch scripts/fetch-stats.sh before batch mode, and prefer a pinned or locally trusted ClawHub CLI instead of npx clawhub@latest.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
