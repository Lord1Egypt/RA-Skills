## Description: <br>
Claw Deep Research turns an AI agent into a multi-phase research assistant that searches iteratively, identifies contradictions, cross-verifies findings, and writes structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[midboss1028-beep](https://clawhub.ai/user/midboss1028-beep) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run deeper research workflows on broad or complex topics. It helps an agent plan searches, inspect gaps and contradictions, verify important claims, and deliver concise summaries with detailed Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-running or background research may continue outside the user's immediate attention and consume many search or fetch operations. <br>
Mitigation: Confirm research depth and background execution before starting, and monitor spawned research sessions for long investigations. <br>
Risk: Research reports or cache files may contain sensitive topics or source material saved locally. <br>
Mitigation: Use non-confidential topics unless storage locations are controlled; review, relocate, or delete generated reports and caches after completion. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/midboss1028-beep/claw-deep-research) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [dzhng/deep-research](https://github.com/dzhng/deep-research) <br>
- [MiroMind](https://dr.miromind.ai) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Brief chat summary plus a structured Markdown research report saved to a local file when possible.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include scope, methodology, findings, contradictions, synthesis, limitations, and source links; file output falls back from Desktop to workspace, temp directory, or chat when storage is unavailable.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
