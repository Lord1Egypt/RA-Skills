## Description: <br>
A RESTful service for high-quality text-to-speech using Qwen3 and specialized voice cloning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hudeven](https://clawhub.ai/user/hudeven) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run a local FastAPI text-to-speech service, synthesize WAV audio from text, and reuse a configured reference voice prompt for voice cloning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can be misused for impersonation or misleading speech generation. <br>
Mitigation: Use only reference audio from people who have explicitly consented, and do not use generated speech for fraud, impersonation, or deception. <br>
Risk: Binding the service to a non-local interface can expose the synthesis endpoint to other machines. <br>
Mitigation: Run with --host 127.0.0.1 unless remote access is intentionally required and separately protected. <br>
Risk: Installation and startup may download or load external machine-learning dependencies and models. <br>
Mitigation: Install in an isolated Python environment and review dependency/model sources before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hudeven/chichi-speech) <br>
- [Publisher profile](https://clawhub.ai/user/hudeven) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with CLI commands, HTTP request examples, and Python service configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The running service returns audio/wav responses from the /synthesize endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
