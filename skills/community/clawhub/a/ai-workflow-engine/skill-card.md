## Description: <br>
AI Workflow Engine helps agents build and run AI workflow automation for task orchestration, agent collaboration, RAG knowledge bases, data processing, and workflow code generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to draft, configure, and execute data-processing, RAG, multi-agent, scheduled, and webhook-driven workflows from natural-language or Python definitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary reports broad network, file, database, webhook, and model-provider actions with insufficient scoping guidance. <br>
Mitigation: Review each generated workflow before execution, run first in a sandbox with test data, and avoid production databases, email, and webhook targets until behavior is validated. <br>
Risk: The server security guidance notes sensitive credentials are required for some model providers and integrations. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid committing secrets, and limit API keys and database credentials to the minimum required permissions. <br>
Risk: The server security summary flags undeclared local imports and the artifact includes hard-coded local skill import paths. <br>
Mitigation: Remove or review local path imports and pin declared dependencies before trusting the skill in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiuwenxi416488212-ship-it/ai-workflow-engine) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill description](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow definitions, generated Python code, data-processing outputs, charts, database operations, model-provider calls, webhook requests, and configuration values depending on the workflow being executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
