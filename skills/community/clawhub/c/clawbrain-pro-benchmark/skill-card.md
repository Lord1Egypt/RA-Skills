## Description: <br>
ClawBrain Benchmark helps evaluate an OpenClaw agent across 205 real-world scenarios and compare results against the ClawBrain v1.0 orchestration engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelfeng](https://clawhub.ai/user/michaelfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams using OpenClaw use this skill to run benchmark-style evaluations covering file operations, search, messaging, terminal workflows, multi-step tasks, error recovery, ambiguous prompts, and visual understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The benchmark may run commands, use network requests, and exercise broad tool workflows. <br>
Mitigation: Run it only in an intentional benchmark session, preferably in a disposable or sandboxed workspace. <br>
Risk: The skill text may not define explicit confirmation prompts, dry-run behavior, or limits around messaging and service-management actions. <br>
Mitigation: Review the skill text before use and add operational limits or confirmation requirements in the host agent policy. <br>


## Reference(s): <br>
- [ClawBrain OpenClaw model comparison report](https://clawbrain.dev/blog/openclaw-model-comparison) <br>
- [ClawHub skill page](https://clawhub.ai/michaelfeng/clawbrain-pro-benchmark) <br>
- [Publisher profile](https://clawhub.ai/user/michaelfeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or text responses with possible shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require curl and may exercise network requests, command execution, and other tool workflows during benchmarking.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
