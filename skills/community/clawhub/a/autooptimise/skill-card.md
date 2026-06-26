## Description: <br>
Autonomously optimises OpenClaw skills by benchmarking outputs, scoring them, proposing targeted SKILL.md changes, and re-testing approved changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wealthvisionai-source](https://clawhub.ai/user/wealthvisionai-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use Autooptimise to benchmark an installed OpenClaw skill, identify low-scoring behavior, and review targeted improvements before approving any SKILL.md changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live benchmark runs can exercise target-skill tools and may interact with account-connected or mutating capabilities. <br>
Mitigation: Confirm the exact target skill and planned tools before each run, and avoid heartbeat scheduling for account-connected or mutating skills. <br>
Risk: The skill proposes changes to other skills, which could introduce misleading guidance or broaden authority if accepted without review. <br>
Mitigation: Review every proposed diff before approval and check that changes do not weaken safety rules or expand permissions. <br>
Risk: Benchmark prompts and scoring choices can steer optimization toward narrow measured behavior instead of overall skill quality. <br>
Mitigation: Review benchmark prompts and scoring output before relying on results, and validate accepted changes in normal agent use. <br>


## Reference(s): <br>
- [Autooptimise on ClawHub](https://clawhub.ai/wealthvisionai-source/autooptimise) <br>
- [README](README.md) <br>
- [Runner instructions](runner/run_experiment.md) <br>
- [Scoring rubric](benchmark/scorer.md) <br>
- [Benchmark tasks](benchmark/tasks.json) <br>
- [autoresearch](https://github.com/karpathy/autoresearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON scoring records and unified diffs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human approval before applying proposed changes; logs benchmark iterations.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and artifact changelog, released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
