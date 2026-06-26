## Description: <br>
Fetches and summarizes recent arXiv and Hugging Face papers with Agentic Paper Digest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matanle51](https://clawhub.ai/user/matanle51) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and research teams use this skill to configure topics, fetch recent papers from arXiv and Hugging Face, and produce paper digests for agent workflows. It can run as a CLI workflow for JSON output or as a local API when polling is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts load environment variables from a configurable ENV_FILE and may expose sensitive API keys if pointed at an untrusted file. <br>
Mitigation: Keep .env private, use a limited API key, and only set ENV_FILE to a trusted local file. <br>
Risk: The stop script targets processes using port 8000 or matching the paper_finder server command and could stop an unintended local service. <br>
Mitigation: Check what is using port 8000 before running the stop script, or stop the intended service manually. <br>
Risk: Bootstrap downloads and installs code and dependencies from the linked project. <br>
Mitigation: Install only after reviewing the linked project and its dependencies in a trusted workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/matanle51/agentic-paper-digest-skill) <br>
- [Agentic Paper Digest GitHub project](https://github.com/matanle51/agentic_paper_digest) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-producing CLI/API workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3, network access, and an OpenAI or OpenAI-compatible API key; CLI runs can create a local SQLite data store under PROJECT_DIR.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
