## Description: <br>
A decision-support agent skill that helps users classify decision type, choose a basic decision framework, compare at least two options, flag common cognitive-bias signals, and label analysis confidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to structure product, technical, business, and personal trade-off decisions. It is intended for single-session decision analysis using basic frameworks and lightweight cognitive-bias checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package declares exec and write tool access even though the documented behavior is Markdown decision-support guidance. <br>
Mitigation: Install only after review, prefer a revised release that removes unnecessary exec/write permissions, or run it in an environment where command execution and file writes are restricted. <br>
Risk: Decision recommendations may be incomplete or misleading when user-provided facts, options, or constraints are incomplete. <br>
Mitigation: Treat outputs as decision support, verify assumptions and confidence labels, and require human review before acting on high-impact decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/decision-architect-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown decision analysis with option comparison tables, bias notes, confidence labels, and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes pure Markdown agent guidance and does not require API keys or network requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
