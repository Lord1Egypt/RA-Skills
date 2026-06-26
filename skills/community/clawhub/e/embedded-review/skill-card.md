## Description: <br>
Expert code review for embedded/firmware projects with dual-model cross-review (Claude + Codex via ACP). Detects memory safety, interrupt hazards, RTOS pitfalls, hardware interface bugs, and C/C++ anti-patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylongw](https://clawhub.ai/user/ylongw) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and firmware engineers use this skill to review embedded code changes for memory safety, interrupt and concurrency correctness, hardware interface defects, C/C++ pitfalls, and embedded security concerns. It can produce single-model reviews for small diffs or dual-model cross-review reports for larger or critical firmware changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review diffs may contain proprietary or secret-bearing code and can be shared with fallback or second-model review tools. <br>
Mitigation: Use Codex-only review, pass --fallback-reviewer none, and consider --no-yolo or equivalent restricted execution when reviewing sensitive repositories. <br>
Risk: Generated review findings can be incorrect, incomplete, or overly cautious for hardware-specific firmware behavior. <br>
Mitigation: Have an embedded engineer validate findings against the target MCU, RTOS, compiler, hardware documentation, and test results before blocking or changing firmware. <br>


## Reference(s): <br>
- [Memory Safety Checklist](references/memory-safety.md) <br>
- [Interrupt Safety Checklist](references/interrupt-safety.md) <br>
- [Hardware Interface Checklist](references/hardware-interface.md) <br>
- [C/C++ Pitfalls Checklist](references/c-pitfalls.md) <br>
- [Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity](https://arxiv.org/abs/2602.03794) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with severity-ranked findings and optional shell commands for diff preparation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review output includes target context, files reviewed, review mode, findings, cross-review analysis when applicable, hardware and timing concerns, architecture notes, and next-step options.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
