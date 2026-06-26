## Description: <br>
ExpertPack Eval measures ExpertPack EK ratio and runs automated quality evaluations for pack-powered agents using blind probing and LLM-as-judge scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ExpertPack maintainers use this skill to measure how much of a pack contains esoteric knowledge and to compare pack-powered agent responses against an evaluation set. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pack propositions, eval questions, expected answers, required facts, and agent responses may be sent to OpenRouter or to configured evaluation endpoints. <br>
Mitigation: Review eval data for secrets before running, use a limited OpenRouter key, and target only trusted endpoints. <br>
Risk: Automated LLM-as-judge scores can be incomplete or wrong. <br>
Mitigation: Treat judge scores as advisory and review YAML results before using them for release or quality decisions. <br>


## Reference(s): <br>
- [ExpertPack Homepage](https://expertpack.ai) <br>
- [ExpertPack Eval on ClawHub](https://clawhub.ai/brianhearn/expertpack-eval) <br>
- [Companion ExpertPack Skill](https://clawhub.ai/skills/expertpack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python shell commands and YAML result files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scripts produce EK ratio summaries, per-proposition scores, aggregate quality metrics, latency data, token counts, and optional manifest/frontmatter values for ExpertPack workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
