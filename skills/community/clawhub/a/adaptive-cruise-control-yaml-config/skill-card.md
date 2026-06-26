## Description: <br>
Use this skill when reading or writing YAML configuration files, loading vehicle parameters, or handling config file parsing with proper error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to read, write, and load YAML configuration files with safe parsing, readable output formatting, default handling, and parse-error recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A syntactically safe YAML load can still accept unexpected keys, invalid value types, unsafe ranges, or untrusted file contents. <br>
Mitigation: Validate allowed keys, expected types, acceptable ranges, and file provenance before using loaded configuration values, especially for sensitive, financial, operational, or vehicle-related settings. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
