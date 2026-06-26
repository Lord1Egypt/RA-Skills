## Description: <br>
Alibaba Cloud PTS (Performance Testing Service) scenario-based skill for creating and managing stress testing scenarios, supporting both PTS native HTTP/HTTPS stress testing and JMeter-based stress testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and performance engineers use this skill to create, run, monitor, verify, and clean up Alibaba Cloud PTS stress testing scenarios for HTTP/HTTPS and JMeter workloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stress tests can send significant traffic to target systems and may affect availability if aimed at unauthorized or production targets. <br>
Mitigation: Use the skill only for systems the user owns or is authorized to test, confirm target URLs and load settings before starting, and begin with low concurrency. <br>
Risk: Cloud permissions can create, start, stop, and delete PTS and JMeter scenarios. <br>
Mitigation: Use least-privilege RAM users or temporary roles and grant only the PTS actions required for the intended workflow. <br>
Risk: Debug logs, scenario definitions, JMeter files, or test data may contain secrets or personal data. <br>
Mitigation: Avoid real secrets or personal data in scenarios and treat debug logs and test artifacts as sensitive. <br>
Risk: PTS scene names are not unique and blind retries after timeouts can create duplicate scenarios or duplicate test runs. <br>
Mitigation: Track SceneId values, check existing status before writes, and disambiguate uncertain outcomes with the user before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-pts-ops) <br>
- [Aliyun CLI installation and configuration](references/cli-installation-guide.md) <br>
- [PTS API and CLI command reference](references/related-apis.md) <br>
- [PTS RAM permission policies](references/ram-policies.md) <br>
- [PTS operation verification methods](references/verification-method.md) <br>
- [PTS scene JSON structure reference](references/pts-scene-json-reference.md) <br>
- [Skill acceptance criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud CLI documentation](https://help.aliyun.com/zh/cli/) <br>
- [Alibaba Cloud PTS API overview](https://help.aliyun.com/zh/pts/developer-reference/api-pts-2020-10-20-overview) <br>
- [Create a PTS stress testing scenario](https://help.aliyun.com/zh/pts/performance-test-pts-2-0/user-guide/create-a-stress-testing-scenario-6) <br>
- [Create a JMeter scenario](https://help.aliyun.com/zh/pts/performance-test-pts-2-0/user-guide/create-a-jmeter-scenario) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Aliyun CLI command guidance and scenario JSON examples for user-approved PTS operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
