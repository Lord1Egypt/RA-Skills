## Description: <br>
Dual Memory combines OpenClaw memory-core with external providers such as SuperMemory so agents can use local QMD search, MEMORY.md, dreaming consolidation, and cloud persistence from one memory slot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dobrinalexandru](https://clawhub.ai/user/dobrinalexandru) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this memory plugin to combine local memory-core recall and dreaming with SuperMemory cloud persistence through a single memory provider slot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud memory capture can store sensitive workspace or conversation content with SuperMemory when autoCapture or broad capture modes are enabled. <br>
Mitigation: Avoid autoCapture or captureMode "everything" in workspaces containing secrets, customer data, proprietary code, or regulated information unless storing that material with the cloud provider is acceptable. <br>
Risk: Cloud behavior is delegated to the sibling openclaw-supermemory extension. <br>
Mitigation: Install and review the sibling openclaw-supermemory extension before enabling cloud memory. <br>


## Reference(s): <br>
- [Dual memory ClawHub release](https://clawhub.ai/dobrinalexandru/dual-memory) <br>
- [README](README.md) <br>
- [SuperMemory](https://supermemory.com) <br>
- [SuperMemory ClawHub skill](https://clawhub.ai/skills/supermemory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Memory recall text, search result snippets, and OpenClaw configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May merge local memory-core results with SuperMemory cloud results when cloud memory is configured.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata; artifact frontmatter is 1.0.7 and package.json is 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
