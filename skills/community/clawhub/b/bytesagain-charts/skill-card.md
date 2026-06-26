## Description: <br>
Bytesagain Charts helps agents generate ASCII, SVG, and HTML charts from CSV, JSON, or pasted data for trend analysis, dashboards, and distribution summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business users can use this skill to turn small datasets or CSV/JSON inputs into terminal charts, SVG/HTML chart files, and chart-selection guidance for reports and dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chart titles, filenames, and usage history may persist locally after generation. <br>
Mitigation: Use non-sensitive chart labels for confidential work and review or clear the local chart-generator history directory after use. <br>
Risk: Generated HTML/SVG output can include user-provided labels or titles. <br>
Mitigation: Use trusted CSV/JSON or pasted labels, inspect generated HTML/SVG before sharing, and avoid opening unreviewed outputs in sensitive browser contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xueyetianya/bytesagain-charts) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [Data visualization best practices](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated ASCII, SVG, or HTML chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with bash and python3; generated chart history may persist under the user's chart-generator data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
