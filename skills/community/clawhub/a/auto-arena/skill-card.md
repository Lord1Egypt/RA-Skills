## Description: <br>
Auto Arena helps agents benchmark and rank multiple AI models or agents for a custom task by generating test queries and rubrics, collecting endpoint responses, running pairwise judge comparisons, and producing reports and charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloml0326](https://clawhub.ai/user/helloml0326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare, benchmark, or rank multiple OpenAI-compatible model or agent endpoints on a custom task without pre-existing test data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Benchmark prompts, model responses, rubrics, and detailed comparison files may contain sensitive task or endpoint data. <br>
Mitigation: Use non-sensitive benchmark data unless the configured providers and local storage settings are appropriate for the data, and disable or clean saved detail files when needed. <br>
Risk: The workflow depends on external AI endpoints and API keys. <br>
Mitigation: Use dedicated API keys with limits, configure provider credentials through environment variables, and run the evaluation in a controlled environment. <br>
Risk: The prerequisite package is installed from Python packaging infrastructure before use. <br>
Mitigation: Verify the py-openjudge package and its dependencies before installation. <br>


## Reference(s): <br>
- [Auto Arena Guide](https://agentscope-ai.github.io/OpenJudge/applications/auto_arena/) <br>
- [Auto Arena on ClawHub](https://clawhub.ai/helloml0326/auto-arena) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with YAML, Python, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide generation of local JSON result files, Markdown reports, charts, and checkpoint files when the referenced AutoArena pipeline is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
