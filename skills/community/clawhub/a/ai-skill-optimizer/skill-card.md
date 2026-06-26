## Description: <br>
Helps agents baseline, analyze, optimize, and verify other skills for token use, performance, security hardening, quality, and regression protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect existing skill artifacts, propose or apply optimization changes, and compare baseline and post-change metrics. It covers token reduction, latency and throughput improvement, security hardening, quality improvement, rollback, and publish preparation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to modify, roll back, package, or publish other skill artifacts without clear approval gates. <br>
Mitigation: Use it only in an isolated workspace, name one target skill explicitly, review diffs before any write, and require separate confirmation for rollback, packaging, and publishing. <br>
Risk: The skill inspects and changes other skill artifacts, which can propagate incorrect guidance or regressions if changes are accepted unreviewed. <br>
Mitigation: Run baseline and post-change comparisons, scan the changed skill before deployment, and keep rollback and publish steps manual. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/johnsmithfan/ai-skill-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/johnsmithfan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON schemas, command examples, checklists, and report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces proposals, metrics summaries, task payloads, rollback guidance, and publish commands for review before execution.] <br>

## Skill Version(s): <br>
1.1.0-en2 (source: server release metadata; artifact frontmatter is 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
