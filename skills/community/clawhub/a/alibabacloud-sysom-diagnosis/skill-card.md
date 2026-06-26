## Description: <br>
Use when troubleshooting Linux server performance or stability issues, including CPU saturation, high load, scheduling delay, memory pressure, OOM events, high RSS, page cache or shared memory growth, memory cgroup residue, Java heap issues, disk IO saturation or latency, packet loss, network jitter, or a server that is slow, stuck, or unstable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, and operations engineers use this skill to route Linux ECS performance and stability symptoms through SysOM diagnosis commands and summarize evidence-backed root causes and next actions. It is intended for Alibaba Cloud SysOM troubleshooting, not for automatically applying repairs. <br>

### Deployment Geography for Use: <br>
China Mainland regions and China (Hong Kong) for remote diagnosis; local diagnosis depends on the supported target operating systems. <br>

## Known Risks and Mitigations: <br>
Risk: The skill may fetch a root-level installer from an Alibaba Cloud OSS URL and pipe it to sudo when sysom-osops is missing. <br>
Mitigation: Install sysom-osops through a verified channel before using the skill, or require explicit review and approval of the installer before any elevated installation step. <br>
Risk: Remote diagnosis requires Alibaba Cloud credentials and an online Cloud Assistant on the target ECS instance. <br>
Mitigation: Configure credentials outside the conversation, use least-privilege RAM policies, and treat authentication or permission errors as setup issues rather than asking the agent to collect secrets. <br>
Risk: SysOM diagnosis may produce remediation recommendations for production systems. <br>
Mitigation: Keep the skill in diagnostic mode by default and review operational actions, ownership, and change-window requirements before executing any repair. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-sysom-diagnosis) <br>
- [Classify Output Guide](references/classify-output-guide.md) <br>
- [Deep Actions Reference](references/deep-actions.md) <br>
- [Memory Triage](references/memory-triage.md) <br>
- [Non-Memory Triage](references/non-memory-triage.md) <br>
- [Parameter Guide](references/parameter-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Report Interpretation](references/report-interpretation.md) <br>
- [Supported Environments](references/supported-environments.md) <br>
- [SysOM CLI Installer](https://sysom-prd-cn-hangzhou.oss-cn-hangzhou.aliyuncs.com/sysom_prd/skill_cli/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise diagnostic summaries and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should preserve SysOM evidence qualifiers and avoid executable remediation snippets unless the user explicitly requests commands.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
