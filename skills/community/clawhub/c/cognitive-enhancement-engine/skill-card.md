## Description: <br>
AI Agent cognitive enhancement engine with working memory, TF-IDF vector memory, planning, reasoning, reflection, and metacognitive monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chen-feng123](https://clawhub.ai/user/chen-feng123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add local memory, retrieval, planning, reasoning, reflection, and runtime status capabilities to Python-based agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can modify a user's shell startup file by adding a shell alias. <br>
Mitigation: Inspect scripts/setup.sh before running it, or use engine.py directly to avoid shell profile changes. <br>
Risk: The engine is designed to retain and recall user-provided text during runtime. <br>
Mitigation: Do not store secrets or sensitive data in the engine's memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chen-feng123/cognitive-enhancement-engine) <br>
- [API specification](references/API_SPEC.md) <br>
- [Use guide](references/USE_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Python objects and text, with Markdown documentation and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python standard-library implementation; runtime memory stores user-provided text in process.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
