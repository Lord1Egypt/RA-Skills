## Description: <br>
Turns raw mistakes, corrections, discoveries, and repeated decisions into structured learnings and promotion candidates while keeping human review before long-term file edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timothysong0w0](https://clawhub.ai/user/timothysong0w0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture lessons from agent work, score and deduplicate them, and draft reviewed patches for long-term behavior or memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated promotion patches could introduce incorrect or overbroad long-term behavior or memory. <br>
Mitigation: Review every generated patch before approval and promote only entries that are clearly supported by evidence. <br>
Risk: Untrusted or hand-crafted patch JSON could modify local agent files unexpectedly during the apply step. <br>
Mitigation: Use reviewed pipeline outputs, run apply steps with --dry-run first, and avoid untrusted patch inputs. <br>


## Reference(s): <br>
- [Learning Store Layout](references/learning-store-layout.md) <br>
- [Scoring Rubric](references/scoring-rubric.md) <br>
- [Promotion Targets](references/promotion-targets.md) <br>
- [Phase 2 Roadmap](references/phase-2-roadmap.md) <br>
- [Phase 3 Roadmap](references/phase-3-roadmap.md) <br>
- [ClawHub Release Page](https://clawhub.ai/timothysong0w0/claw-self-improving-plus) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON records, patch candidates, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable learning records, backlog summaries, and candidate patches; approved patches may update SOUL.md, AGENTS.md, TOOLS.md, or MEMORY.md.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
