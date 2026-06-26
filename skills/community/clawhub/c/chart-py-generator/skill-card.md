## Description: <br>
Generates data visualization charts with Python matplotlib, supporting seven chart types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttguy0707](https://clawhub.ai/user/ttguy0707) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to turn numeric data into local chart images for reports, summaries, and comparisons. It supports line, bar, pie, scatter, area, multi-line, and grouped bar charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Charts can contain sensitive source data, and the documentation includes optional Telegram-send examples. <br>
Mitigation: Use the local chart generation workflow for sensitive data and only send chart images externally when the data is approved for that destination. <br>
Risk: The generator writes chart images to a caller-selected output path. <br>
Mitigation: Choose output paths deliberately and review generated files before sharing or attaching them to downstream workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ttguy0707/chart-py-generator) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Chart generator script](artifact/chart_gen.py) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated chart image files such as PNG] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python and matplotlib; chart type, data, labels, title, dimensions, color, and output path are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
