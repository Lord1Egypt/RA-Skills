## Description: <br>
Dual-brain memory skill for correction handling, rewrite quality, post-task reflection, and semantic recall of historical pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenni666](https://clawhub.ai/user/chenni666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to maintain cross-session rule memory, capture corrections and task reflections, and retrieve semantically related pitfalls before or during work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to persist cross-session memory in local Markdown files and Pinecone records. <br>
Mitigation: Use it only when persistent memory is desired, start with a non-production tenant, and review or clear ~/dual-brain-memory-guardian and the Pinecone namespace when retention is no longer wanted. <br>
Risk: The runtime requires a Pinecone API key. <br>
Mitigation: Use a limited-scope key, provide it through environment configuration, and avoid placing secrets or sensitive personal data in prompts, memory content, or logs. <br>
Risk: Corrections, reflections, and recalls may contain sensitive or outdated context if stored without review. <br>
Mitigation: Follow the artifact's redaction and boundary guidance, keep Pinecone recall advisory rather than authoritative, and promote only explicit stable rules into Markdown. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chenni666/dual-brain-memory-guardian) <br>
- [Publisher Profile](https://clawhub.ai/user/chenni666) <br>
- [Node.js Download](https://nodejs.org/en/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with npm shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory workflow guidance and command proposals; runtime commands may read or write local Markdown memory and Pinecone records.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
