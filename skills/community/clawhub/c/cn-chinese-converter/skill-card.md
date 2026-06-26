## Description: <br>
Cn Chinese Converter converts Chinese text between Simplified and Traditional variants locally, including Taiwan and Hong Kong variants, with optional JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to convert Chinese text between Simplified and Traditional forms for regional localization, including Taiwan and Hong Kong variants. It is useful for local, command-line text conversion workflows that do not require network access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter depends on the third-party Python package opencc-python-reimplemented. <br>
Mitigation: Review and install the dependency from an approved package source before running the script. <br>
Risk: The documented examples may not match the script's --direction command-line argument. <br>
Mitigation: Use the script's supported --direction values, such as t2s, s2t, t2tw, and t2hk, when invoking conversion. <br>
Risk: The skill documentation includes promotional external links. <br>
Mitigation: Treat those links as external publisher content and not as part of the local text conversion workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-chinese-converter) <br>
- [Publisher profile](https://clawhub.ai/user/freedompixels) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON from a local command-line converter, with Markdown usage guidance when invoked by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Conversion requires Python and the opencc-python-reimplemented package; documented examples may need adjustment to use the script's --direction argument.] <br>

## Skill Version(s): <br>
1.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
