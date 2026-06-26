## Description: <br>
将中国地址按行政区划智能分类为本省本市、本省外市、外省或地址不全，支持不完整地址补全和多格式输入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhh8896416](https://clawhub.ai/user/zhh8896416) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operations teams use this skill to classify Chinese address records by administrative region, especially for Guizhou and Guiyang workflows. It supports batch file processing, configurable target regions, and incomplete-address completion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input files, output files, and DEBUG logs may contain full personal addresses. <br>
Mitigation: Treat these files and logs as sensitive, restrict access, and avoid sharing raw address data outside approved workflows. <br>
Risk: The PyYAML dependency may drift if installed without pinning, and server evidence notes it may be unused. <br>
Mitigation: Install in a virtual environment and pin or remove PyYAML after confirming whether configuration loading requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhh8896416/address-classifier) <br>
- [README](artifact/README.md) <br>
- [Manifest](artifact/MANIFEST.md) <br>
- [Configuration](artifact/config/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples, plus TSV, CSV, or JSON classification output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads UTF-8 address files and writes classified records containing the original address, category, province, city, district, and remarks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-03-09) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
