## Description: <br>
Essence Trace helps agents analyze a claim, phenomenon, or question by repeatedly asking why, applying first principles, and identifying root causes and leverage points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-long-2022](https://clawhub.ai/user/jack-long-2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for Chinese-language root-cause analysis and first-principles reasoning. It is intended for exploring views, phenomena, or questions until the agent can summarize the underlying mechanism and practical leverage points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generic 'why' trigger may activate more often than intended. <br>
Mitigation: Use explicit invocation or confirm the user's intent before applying the full root-cause workflow. <br>
Risk: Root-cause analysis can overstate causality for complex, subjective, or value-based topics. <br>
Mitigation: Review the assumptions in each question chain, distinguish evidence from judgment, and stop at clearly marked value or boundary conditions. <br>
Risk: The skill is written for Chinese-language use and may be difficult for non-Chinese users. <br>
Mitigation: Translate or localize the prompts and output labels before deploying it for non-Chinese users. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jack-long-2022/skills/essence-trace) <br>
- [Detailed process](artifact/PROCESS.md) <br>
- [Housing analysis example](artifact/examples/case-1-housing.md) <br>
- [Second-curve analysis example](artifact/examples/case-2-second-curve.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown response with a question chain, indivisible node, leverage points, and essence summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language, text-only reasoning output; no code execution or shell commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
