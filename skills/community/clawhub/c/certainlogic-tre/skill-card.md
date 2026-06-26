## Description: <br>
Provides a local Python answer cache for repeated LLM queries, with uncertainty checks intended to avoid caching hedged responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to cache repeated LLM answers locally, retrieve cache hits before making new model calls, inspect cache metrics, and avoid storing responses that contain obvious hedging language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores LLM answers persistently on local disk, which can expose secrets, personal data, regulated data, or proprietary responses if users cache sensitive outputs. <br>
Mitigation: Use it only with data approved for local persistence, isolate and manage the cache location, and clear or disable persistence for sensitive workflows. <br>
Risk: The security review reports that some advertised safety and configuration controls are not implemented by the included code. <br>
Mitigation: Do not rely on this skill as a complete command blocker, intent gate, tamper-proof cache, facts database, or fully configurable gateway unless those controls are separately verified. <br>
Risk: Cached answers can become stale or incorrect and may be returned without a fresh model call. <br>
Mitigation: Set conservative cache lifetimes for volatile information and review cached content before using it for consequential decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/certainlogicai/certainlogic-tre) <br>
- [Publisher profile](https://clawhub.ai/user/certainlogicai) <br>
- [API reference](artifact/references/API.md) <br>
- [Configuration guide](artifact/references/CONFIGURATION.md) <br>
- [Token Reduction Engine homepage](https://certainlogic.ai/tre) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell install commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Python cache behavior and metrics guidance; cached answers are persisted to disk by the bundled module.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
