## Description: <br>
Activate when user asks how to discuss product/strategy questions, requests analysis of unfamiliar markets, or when sparse documentation might tempt extrapolation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tatsuko-tsukimi](https://clawhub.ai/user/tatsuko-tsukimi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill during product, strategy, research, and technical critique conversations to keep analysis grounded in evidence, avoid stale external-state claims, and avoid over-synthesizing sparse material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to search the web using terms from a user's prompt during market, research, or current-state verification. <br>
Mitigation: Avoid including confidential project names or sensitive details in prompts that may be searched unless the host agent redacts or withholds those terms. <br>
Risk: The skill can cause the agent to withhold strong conclusions when evidence is sparse or current external facts have not been checked. <br>
Mitigation: Use it where grounded analysis is more important than fast speculation, and explicitly state when a speculative answer is desired. <br>


## Reference(s): <br>
- [Epistemic Hygiene Skill Page](https://clawhub.ai/tatsuko-tsukimi/epistemic-hygiene) <br>
- [Principles](references/principles.md) <br>
- [Triggers](references/triggers.md) <br>
- [Anti-patterns Catalog](references/anti-patterns-catalog.md) <br>
- [Research Before Assertion Example](examples/research-before-assertion.md) <br>
- [Sparse Evidence Example](examples/sparse-evidence.md) <br>
- [Market Claim Verification Example](examples/market-claim-verification.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text or Markdown analytical guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies reasoning principles silently by default and surfaces brief epistemic notes when needed to avoid misleading the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
