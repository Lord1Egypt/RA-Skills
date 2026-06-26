## Description: <br>
Chart Toolkit helps agents create and export Python-based line, bar, pie, candlestick, heatmap, dashboard, and interactive HTML visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operations teams use this skill to generate charts, dashboards, and report exports from local Python data workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unpinned Python dependencies can change behavior across environments. <br>
Mitigation: Pin and review runtime dependencies before using the skill in production workflows. <br>
Risk: Generated HTML reports can expose users to unsafe content if untrusted data is inserted without escaping. <br>
Mitigation: Escape or sanitize untrusted data before writing it into generated HTML dashboards or reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiuwenxi416488212-ship-it/chart-toolkit) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and file output paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local PNG, HTML, PDF-style report artifacts, dashboards, and base64-encoded chart images when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
