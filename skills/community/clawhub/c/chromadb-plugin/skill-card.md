## Description: <br>
Integrates ChromaDB vector storage with OpenClaw for local vector memory, LanceDB-compatible access, migration tooling, and hybrid search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lulan3954-a11y](https://clawhub.ai/user/lulan3954-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure ChromaDB as a local vector memory backend, test the integration, and migrate existing LanceDB memory data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin persists and migrates private OpenClaw memory data. <br>
Mitigation: Back up existing LanceDB and OpenClaw data, test migration on a copy first, and avoid using production or sensitive memory stores until review is complete. <br>
Risk: Remote ChromaDB configuration can expose memory data or credentials if handled carelessly. <br>
Mitigation: Prefer local ChromaDB mode for private memory, protect any ChromaDB API key, and keep generated configuration files out of source control. <br>
Risk: The security summary flags under-disclosed safety limits and an undocumented query trigger. <br>
Mitigation: Review the Python scripts and query behavior before deployment, and remove or disable behavior that is not acceptable for the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lulan3954-a11y/chromadb-plugin) <br>
- [Publisher profile](https://clawhub.ai/user/lulan3954-a11y) <br>
- [Quick Start Guide](artifact/docs/quick_start_en.md) <br>
- [Configuration example](artifact/config.example.yaml) <br>
- [Original declaration](artifact/ORIGINAL_DECLARATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, configuration, testing, migration, and vector-store integration guidance for an agent.] <br>

## Skill Version(s): <br>
v1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
