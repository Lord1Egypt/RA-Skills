## Description: <br>
Make your agent get better on its own by setting up golden tests, running automated evaluations, and tracking improvement over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dario-github](https://clawhub.ai/user/dario-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to define golden tests, evaluate agent behavior, compare ablation conditions, and identify regressions or weak dimensions before changing an agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can delete the configured installation directory during a failed update. <br>
Mitigation: Review the install script before use and set EVOLUTION_INSTALL_DIR only to a dedicated, non-critical directory. <br>
Risk: Evaluation runs may exercise agent files, prompts, or memory content that should not be altered during testing. <br>
Mitigation: Run tests against copies or sandboxed agent files and use a dedicated LLM API key for judging. <br>
Risk: Installing directly from a moving repository can change behavior between installs. <br>
Mitigation: Install from a reviewed, pinned commit or release when using the skill in a controlled environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dario-github/agent-self-evolution) <br>
- [Project Homepage](https://github.com/dario-github/agent-self-evolution) <br>
- [nous-safety Companion Project](https://github.com/dario-github/nous) <br>
- [biomorphic-memory Companion Project](https://github.com/dario-github/biomorphic-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python >= 3.11 and an LLM API key for evaluation judging.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
