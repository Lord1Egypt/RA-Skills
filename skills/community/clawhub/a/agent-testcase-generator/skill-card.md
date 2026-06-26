## Description: <br>
Generates standardized functional, API, and UI automation test cases from test points using a required 14-field format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luiciferyi](https://clawhub.ai/user/luiciferyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, developers, and test designers use this skill to turn feature modules or test-point lists into detailed, standardized test cases with preconditions, steps, expected results, verification points, priorities, boundary cases, exception cases, and automation markers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated test cases can be written to a configured Feishu knowledge base, which may store sensitive test requirements or internal system details. <br>
Mitigation: Confirm the listed Feishu workspace and wiki node before use, and avoid providing information that should not be stored there. <br>
Risk: The skill is expected to produce Chinese-format output unless another language is requested. <br>
Mitigation: Request the desired output language explicitly before generating or publishing test cases. <br>


## Reference(s): <br>
- [Agent Testcase Generator documentation](artifact/agent-testcase-generator.md) <br>
- [Standard test case format](artifact/测试用例标准格式.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown-style test cases using the required 14-field format] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update Feishu documents when the configured workspace is intended.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
