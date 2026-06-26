## Description: <br>
Finds the core ideas that survive across multiple sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leegitw](https://clawhub.ai/user/leegitw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and knowledge workers use this skill to synthesize three or more related sources into invariant principles, domain-specific findings, and Golden Master candidates for later human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Synthesized outputs can retain confidential details, mistakes, or bias from the provided sources. <br>
Mitigation: Only provide source text that may be processed by the configured model provider, and review outputs before treating them as canonical or sharing them. <br>
Risk: Golden Master candidates are consistency signals, not proof of correctness. <br>
Mitigation: Use candidates as evidence for human judgment and verify them before adopting them as a source of truth. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leegitw/core-refinery) <br>
- [Project homepage](https://github.com/live-neon/skills/tree/main/pbd/core-refinery) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown narrative with optional structured JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill does not write files. Outputs may include source hashes, N-counts, synthesis metrics, next steps, and share text when Golden Master candidates are found.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
