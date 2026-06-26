## Description: <br>
Unified LLM Council skill that installs, queries, and manages a multi-model consensus app for synthesized answers through a quick CLI or web UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeadland](https://clawhub.ai/user/jeadland) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to install and operate a local LLM Council app, then submit questions to multiple LLMs and receive a synthesized chairman answer. It also provides status and stop commands for the local backend and frontend services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer clones and runs an external llm-council repository and installs backend and frontend dependencies. <br>
Mitigation: Install only if you trust the external repository and review the cloned project before running it with credentials. <br>
Risk: The skill reads or writes LLM credentials and can send prompts to a local gateway or model provider. <br>
Mitigation: Use dedicated credentials where possible and avoid entering sensitive prompts or secrets unless the backend and provider handling are acceptable. <br>
Risk: The installer may stop existing listeners on ports 8001, 5173, or 4173 while starting its services. <br>
Mitigation: Check those ports before install and stop or move important local services first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeadland/council-brief) <br>
- [LLM Council repository](https://github.com/jeadland/llm-council) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start local backend and frontend processes, write local configuration, and return links to the full discussion UI.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
