## Description: <br>
Iteratively rewrites essays to reduce AI-detector false positives while preserving meaning, citations, and natural writing style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin0818-lxd](https://clawhub.ai/user/kevin0818-lxd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and writing-support agents use this skill to measure essay style signals, generate targeted rewrites, and return a final essay with an iteration report while preserving the original argument and citations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to misrepresent authorship or bypass school, workplace, platform, or review policies. <br>
Mitigation: Use it only for permitted style revision and false-positive reduction, and follow applicable disclosure or authorship policies. <br>
Risk: Broad writing-help triggers may activate the workflow for requests where AI-detection evasion is inappropriate. <br>
Mitigation: Narrow triggers or add explicit acceptable-use checks before allowing the rewrite loop to run. <br>
Risk: Optimizing against AI-detector signals can overfit style metrics instead of improving factual quality. <br>
Mitigation: Manually review the final essay, preserve citations and factual claims, and reject unsupported additions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevin0818-lxd/essay-humanize-iterator) <br>
- [Measurement Metrics](skill/references/metrics.md) <br>
- [Iteration Strategy](skill/references/iteration_strategy.md) <br>
- [AI Writing Patterns](skill/references/patterns.md) <br>
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text essay with a Markdown iteration table and change summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local measurement scripts and returns the best-scoring rewrite within the configured iteration limit.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
