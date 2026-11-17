## Description:

Alibaba Cloud PTS (Performance Testing Service) scenario-based skill for creating and managing PTS native HTTP/HTTPS and JMeter stress testing scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to create, run, monitor, verify, and clean up Alibaba Cloud PTS native and JMeter stress testing scenarios through Aliyun CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Aliyun CLI automatic plugin installation can expand trust for future CLI use.

Mitigation: Prefer a verified, pinned Aliyun CLI installation method and avoid global automatic plugin installation unless that persistent trust expansion is accepted.

Risk: Stress testing can send high-impact traffic to target systems.

Mitigation: Run tests only against systems the user owns or is explicitly authorized to test, use a narrowly scoped RAM role, and require explicit confirmation before execution.

Risk: Scenario JSON and debug logs may expose credentials or sensitive test data.

Mitigation: Avoid real credentials in scenario JSON and redact debug logs before sharing.

## Reference(s):

- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [PTS Scene JSON Reference](references/pts-scene-json-reference.md)
- [PTS RAM Policies](references/ram-policies.md)
- [PTS Related APIs and CLI Commands](references/related-apis.md)
- [PTS Verification Methods](references/verification-method.md)
- [Acceptance Criteria: PTS Stress Testing Scenario Skill](references/acceptance-criteria.md)
- [Official Aliyun CLI Documentation](https://help.aliyun.com/zh/cli/)
- [PTS API Documentation](https://help.aliyun.com/zh/pts/developer-reference/api-pts-2020-10-20-overview)
- [Create a Stress Testing Scenario](https://help.aliyun.com/zh/pts/performance-test-pts-2-0/user-guide/create-a-stress-testing-scenario-6)
- [Create a JMeter Scenario](https://help.aliyun.com/zh/pts/performance-test-pts-2-0/user-guide/create-a-jmeter-scenario)
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-pts-ops)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes user confirmation, idempotency checks, verification steps, and cleanup practices for PTS and JMeter scenarios.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
