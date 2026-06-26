## Description: <br>
Cybernetic Evolver is an AI self-evolution framework based on Tsien's Engineering Cybernetics that implements closed-loop feedback, adaptive control, self-organizing principles, Lyapunov stability protection, structure mutation, and online learning for autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ywewanhuang](https://clawhub.ai/user/ywewanhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to embed an advisory optimization module that evaluates performance signals, selects strategies, adapts parameters, and records feedback for autonomous agents operating in changing environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optimizer can influence agent routing or strategy choices from performance signals. <br>
Mitigation: Keep recommendations advisory unless the host application adds approval gates for real-world or cross-agent actions. <br>
Risk: Persisted optimizer state or performance history can retain sensitive or account-impacting signals. <br>
Mitigation: Restrict save/load paths to a dedicated directory and avoid secrets, private user data, or account-impacting signals without a retention and deletion policy. <br>
Risk: Adaptive learning or structure mutation can produce unsuitable strategies if accepted automatically. <br>
Mitigation: Review proposed strategy changes, bound the actions the host can execute, and scan the skill before deployment. <br>


## Reference(s): <br>
- [Cybernetic Evolver Release Page](https://clawhub.ai/ywewanhuang/cybernetic-evolver) <br>
- [README](artifact/README.md) <br>
- [Architecture](artifact/ARCHITECTURE.md) <br>
- [Workflow](artifact/WORKFLOW.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist optimizer state and performance history when host code calls save/load.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
