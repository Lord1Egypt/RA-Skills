## Description: <br>
基于qgdata API的A股分钟级数据查询服务。提供实时股价、分钟K线、分时数据等专业数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Listolany](https://clawhub.ai/user/Listolany) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading workflow builders use this skill to query A-share minute K-line data and related qgdata-backed stock information from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that setup documentation includes a concrete QGDATA_TOKEN example, which is unsafe credential handling. <br>
Mitigation: Use a separately issued token stored outside version control, ignore any bundled token value, and ask the publisher to replace the example with a placeholder and rotate any exposed credential. <br>
Risk: The skill calls an external qgdata service using user-supplied stock symbols and query parameters. <br>
Mitigation: Review commands before execution, provide only intended market symbols and fields, and keep API credentials scoped to the minimum required access. <br>


## Reference(s): <br>
- [A Stock Info on ClawHub](https://clawhub.ai/Listolany/a-stock-info) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON query output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, qgdata, pandas, and a user-provided QGDATA_TOKEN.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
