## Description: <br>
Alibaba Cloud content moderation and AI guardrails automated testing that runs sample content against moderation APIs, compares services, supports manual annotation and false-negative analysis, tests prompt injection, sensitive data, and jailbreak cases, and generates alignment reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and safety engineers use this skill to configure Alibaba Cloud moderation scenarios, run batch moderation and AI guardrail tests, annotate outcomes, and produce alignment reports for content safety workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Alibaba Cloud moderation configuration when console automation is used. <br>
Mitigation: Use a controlled test or staging Alibaba Cloud account unless production configuration changes are intentional, and review the scenario and label changes before saving. <br>
Risk: The browser automation workflow saves a reusable console login session locally. <br>
Mitigation: Treat the saved browser state as a credential, keep it out of synced folders, and delete it when testing is complete. <br>
Risk: Moderation test samples can contain customer content, secrets, regulated personal data, or confidential URLs. <br>
Mitigation: Use synthetic or approved test data, and submit sensitive or regulated data only when Alibaba Cloud processing is explicitly approved. <br>
Risk: Broad cloud permissions increase the impact of mistakes during service configuration and API testing. <br>
Mitigation: Prefer least-privilege RAM credentials scoped to the required Alibaba Cloud Green moderation actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-safety-checker) <br>
- [Console automation guide](references/console-guide.md) <br>
- [Label configuration matrix](references/label-matrix.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Scenario guide](references/scenarios.md) <br>
- [Alibaba Cloud AI safety guardrail product page](https://www.aliyun.com/product/lvwang) <br>
- [Alibaba Cloud credential chain documentation](https://help.aliyun.com/document_detail/378659.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated JSON, CSV, XLSX, and HTML report files from the bundled scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include request IDs, trace IDs, risk labels, confidence data, annotations, latency, and per-service alignment metrics.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
