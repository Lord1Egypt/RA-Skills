## Description: <br>
安全卫士 v2.1 - 智能威胁检测、权限控制、隐私保护。L1-L4四级安全等级，13种攻击模式自动识别，中央库单点修改全局生效。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xingjihome](https://clawhub.ai/user/xingjihome) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen prompts and messages for security threats, assign L1-L4 trust levels, block or sanitize risky content, and inspect OpenClaw-style security status and configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is defensive, but server security evidence marks it suspicious because it claims read-only protection while retaining scanned content and describing broader local access and high-trust authority. <br>
Mitigation: Review and scan before installing; use restrictive defaults and require explicit approval for file, command, network, or configuration-changing actions. <br>
Risk: The skill may read local OpenClaw or WorkBuddy memory to identify owner information. <br>
Mitigation: Install only where that local memory access is acceptable, keep permissions scoped to the skill and memory directories, and avoid exposing prompt-visible owner identifiers. <br>
Risk: The skill can store snippets of inspected prompts or attack samples. <br>
Mitigation: Disable or regularly clear sample persistence where possible, and avoid sending secrets or sensitive personal data through checks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xingjihome/anquan-weishi) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>
- [Installation guide](artifact/config/install_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, shell commands, configuration] <br>
**Output Format:** [JSON safety-check results plus concise text or Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sanitized content, risk level, matched threats, recommendation, status, or level information.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
