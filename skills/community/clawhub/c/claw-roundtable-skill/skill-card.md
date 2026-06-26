## Description: <br>
RoundTable v3.0 is a multi-agent roundtable discussion engine with heterogeneous model routing, MMR intent parsing, convergence controls, and a 170+ expert library. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krislu1221](https://clawhub.ai/user/krislu1221) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and teams use this skill to run structured multi-agent reviews for technical architecture, product planning, business research, and other complex decisions that benefit from expert disagreement and arbitration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can launch multiple subagents and share the discussion topic plus prior-round summaries with them. <br>
Mitigation: Use it only for topics appropriate for multi-agent processing, avoid secrets or confidential data, and review the generated discussion before acting on it. <br>
Risk: Local OpenClaw model configuration access may expose model-routing details or conflict with the skill's stronger privacy claims. <br>
Mitigation: Prefer explicitly supplied model settings and review local OpenClaw configuration access before installation or execution. <br>
Risk: Optional chat-room broadcasting and report persistence can expose discussion content beyond the immediate session. <br>
Mitigation: Keep broadcasting and persistence disabled unless required, and confirm output locations and audience before enabling them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krislu1221/claw-roundtable-skill) <br>
- [OpenClaw RoundTable documentation](https://docs.openclaw.ai/skills/roundtable) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown reports, structured discussion summaries, code snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May launch multiple subagents and optionally persist reports or broadcast truncated discussion updates when enabled.] <br>

## Skill Version(s): <br>
3.0.13 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
