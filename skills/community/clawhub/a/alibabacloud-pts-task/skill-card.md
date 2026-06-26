## Description: <br>
Executes Alibaba Cloud Performance Testing Service scenario operations for native HTTP/HTTPS and JMeter stress testing, including create, query, start, stop, report, and delete workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage authorized Alibaba Cloud PTS stress-test scenarios through Aliyun CLI workflows, with parameter checks, verification steps, and cleanup guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start real load tests against target systems. <br>
Mitigation: Use it only for systems you own or are authorized to assess, avoid production targets unless explicitly approved, and require final human confirmation before starting tests. <br>
Risk: The skill can stop or delete cloud test scenarios. <br>
Mitigation: Require explicit confirmation before stop or delete operations and verify scenario identity before acting. <br>
Risk: The skill requires sensitive Alibaba Cloud access. <br>
Mitigation: Use a least-privilege RAM role and do not place real tokens or credentials in scene JSON or shared logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-pts-task) <br>
- [Acceptance Criteria: PTS Stress Testing Scenario Skill](references/acceptance-criteria.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [PTS Scene JSON Reference](references/pts-scene-json-reference.md) <br>
- [PTS RAM Policies](references/ram-policies.md) <br>
- [PTS Related APIs and CLI Commands](references/related-apis.md) <br>
- [PTS Verification Methods](references/verification-method.md) <br>
- [PTS API Documentation](https://help.aliyun.com/zh/pts/developer-reference/api-pts-2020-10-20-overview) <br>
- [Create a Stress Testing Scenario](https://help.aliyun.com/zh/pts/performance-test-pts-2-0/user-guide/create-a-stress-testing-scenario-6) <br>
- [Create a JMeter Scenario](https://help.aliyun.com/zh/pts/performance-test-pts-2-0/user-guide/create-a-jmeter-scenario) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown with Aliyun CLI commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Alibaba Cloud PTS scene IDs, report IDs, status summaries, and cleanup steps.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
