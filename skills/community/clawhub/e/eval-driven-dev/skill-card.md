## Description: <br>
Helps developers add instrumentation, build golden datasets, write eval-based tests, run them, root-cause failures, and iterate on Python LLM applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yiouli](https://clawhub.ai/user/yiouli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add evaluation-driven QA to Python LLM applications, including instrumentation, trace capture, golden datasets, eval tests, and failure investigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may upgrade project dependencies or reinstall itself as part of startup checks. <br>
Mitigation: Run it in a branch or disposable environment and require explicit approval before dependency upgrades or skill reinstallation. <br>
Risk: Eval setup can capture prompts, traces, expected outputs, and other sensitive application data in the pixie_qa directory. <br>
Mitigation: Use scoped test API keys, avoid production data where possible, and inspect pixie_qa for secrets or sensitive prompts before committing, sharing, or retaining it. <br>


## Reference(s): <br>
- [Pixie API Reference](artifact/references/pixie-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yiouli/eval-driven-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code edits, shell commands, and generated pixie_qa files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project instrumentation, eval datasets, tests, scripts, and pixie_qa artifacts.] <br>

## Skill Version(s): <br>
0.1.11 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
