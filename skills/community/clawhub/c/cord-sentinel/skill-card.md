## Description: <br>
SENTINEL/CORD governance engine for mandatory pre-flight evaluation of agent tool calls, external input scanning, blocked-action reporting, audit checks, and intent-lock setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zanderone1980](https://clawhub.ai/user/zanderone1980) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to evaluate higher-risk shell, file, browser, network, and message actions before execution, scan external data for prompt injection, and inspect CORD status. It also provides guidance for reporting blocked actions and setting session intent locks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on unbundled CORD engine code that may be loaded from an environment path or local installation. <br>
Mitigation: Review the actual cord_engine source and version before relying on the skill, and avoid setting CORD_ENGINE_PATH to untrusted directories. <br>
Risk: CORD status output may expose recent intents, commands, paths, and network targets. <br>
Mitigation: Treat status output as sensitive and avoid sharing it beyond the operators who need it. <br>


## Reference(s): <br>
- [CORD Python API Reference](references/cord-api.md) <br>
- [ClawHub release page](https://clawhub.ai/zanderone1980/cord-sentinel) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an available cord_engine installation or configured CORD_ENGINE_PATH for status checks.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
