## Description: <br>
OpenClaw continuity kernel for fail-open llm_input injection, deterministic runtime contracts, and shadow-mode eval receipts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to add bounded continuity memory, runtime contract proofs, and shadow-mode evaluation receipts to OpenClaw workflows while preserving fail-open behavior on continuity failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local continuity memory may be reused in future model inputs. <br>
Mitigation: Install only when persistent continuity is desired, avoid storing highly sensitive Soul Card details, and review or clear ~/.local/state/continuity-kernel/continuity.db when needed. <br>
Risk: Evaluation traces and receipts may contain operational context or sensitive task details. <br>
Mitigation: Choose trace and evaluation output paths deliberately and review or clear ~/.cache/continuity-kernel when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkuehnl/continuity-kernel) <br>
- [Publisher profile](https://clawhub.ai/user/tkuehnl) <br>
- [CacheForge skills homepage](https://github.com/cacheforge-ai/cacheforge-skills) <br>
- [README](artifact/README.md) <br>
- [Evaluation receipts](artifact/artifacts/continuity-kernel/p0-evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON files] <br>
**Output Format:** [Markdown guidance with bash commands and machine-readable JSON receipts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local SQLite continuity state and cache/evaluation receipt files when the hooks or commands are run.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
