## Description: <br>
Format Converter Free helps developers and data workers convert single files among CSV, JSON, XML, YAML, and TOML while preserving nested structures, inferring common data types, and handling common text encodings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data workers, operations engineers, and integration engineers use this skill to convert configuration files, API payloads, tabular data, and legacy XML data between common structured-data formats. It is best suited for single-file conversions up to 10 MB. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad execution authority for a task that is primarily local file conversion. <br>
Mitigation: Review commands before execution, install only required dependencies, and run conversions in a controlled workspace. <br>
Risk: Converted output can overwrite or corrupt important configuration or data files if written to the wrong path. <br>
Mitigation: Back up source files, write converted data to a new output path, and validate the result before replacing existing files. <br>
Risk: Callback URLs or external storage credentials could expose local data if provided unintentionally. <br>
Mitigation: Do not provide callback URLs or credentials unless network integration is intended and the destination is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/format-converter-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured data examples, code snippets, and shell-oriented dependency instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces converted structured-data content or instructions for producing converted files; free edition is scoped to one file and recommends files no larger than 10 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
