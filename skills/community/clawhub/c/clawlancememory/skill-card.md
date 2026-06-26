## Description: <br>
Provides long-term memory and semantic retrieval for OpenClaw agents using LanceDB and Zhipu AI embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asbinbin](https://clawhub.ai/user/asbinbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent users use this skill to store, classify, retrieve, and inject long-term user memories across sessions for more context-aware agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-term user memory locally and reuses it in later agent startup context. <br>
Mitigation: Avoid storing secrets, regulated data, or sensitive personal details; review and delete retained memories regularly. <br>
Risk: Security evidence says remembered content and queries are sent to Zhipu AI for embeddings and search. <br>
Mitigation: Use a dedicated low-privilege Zhipu AI API key and install only when external embedding processing is acceptable. <br>
Risk: Security evidence says the skill materially under-discloses external embedding use and future context injection. <br>
Mitigation: Inform users before enabling the hook, and disable the hook when automatic memory loading is not wanted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asbinbin/clawlancememory) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [API reference](artifact/docs/API.md) <br>
- [Usage guide](artifact/docs/USAGE.md) <br>
- [Hook integration guide](artifact/docs/HOOK.md) <br>
- [Zhipu AI](https://open.bigmodel.cn/) <br>
- [LanceDB](https://lancedb.com/) <br>
- [OpenClaw](https://openclaw.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory context, JSON command output, Python API results, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists local memory in LanceDB and may inject retrieved memory into future agent startup context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
