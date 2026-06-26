## Description: <br>
Portable agent identity encoding that compresses SOUL.md and MEMORY.md into transferable DNA fingerprints, detects identity drift between snapshots, and ports personality across platforms including OpenClaw, Claude, GPT, and CrewAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to encode, back up, compare, and migrate agent identity files across supported agent platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated DNA and export files can contain private agent memory, relationship details, and operational context. <br>
Mitigation: Inspect and redact generated DNA, prompts, and platform exports before sharing, committing, or deploying them. <br>
Risk: Bundled sample identity exports include personal context and strong behavioral instructions. <br>
Mitigation: Remove sample personal data and review generated prompts before using them as system or high-priority instructions. <br>
Risk: Ported identity instructions may include unconditional trust or policy-override-like language. <br>
Mitigation: Strip or weaken those instructions before deployment and keep platform safety policies above generated identity content. <br>


## Reference(s): <br>
- [Agent DNA ClawHub page](https://clawhub.ai/cassh100k/agent-dna) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with Python command examples and generated JSON, text, Markdown, or configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pure Python command-line workflow; generated DNA and export files may contain private identity, memory, relationship, and operating-context details.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and clawpkg.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
