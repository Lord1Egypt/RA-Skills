## Description: <br>
Persistent memory for AI agents via getmem.ai. Call mem.get() before each LLM call to inject context, and mem.ingest() after each turn to save the conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimblev2023](https://clawhub.ai/user/nimblev2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add persistent, queryable conversation memory through getmem.ai so agents can retrieve relevant context before a model call and save conversation turns afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation turns may be sent to an external persistent memory service. <br>
Mitigation: Use the skill only when getmem.ai is approved for the conversation data being processed and users have appropriate notice or consent. <br>
Risk: Secrets, regulated data, or confidential conversations could be stored in persistent memory. <br>
Mitigation: Disable the skill for sensitive sessions and filter or redact sensitive content before calling mem.ingest(). <br>
Risk: The artifact states that memory persists indefinitely and provides no TTL or purge behavior. <br>
Mitigation: Confirm deletion and export controls with getmem.ai before deployment and define an operational retention process. <br>
Risk: The skill requires a GETMEM_API_KEY credential. <br>
Mitigation: Store the key in a managed secret store or environment variable, rotate it on exposure, and avoid committing it to source files or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nimblev2023/getmem) <br>
- [getmem.ai website](https://getmem.ai) <br>
- [getmem.ai platform](https://platform.getmem.ai) <br>
- [getmem-ai on PyPI](https://pypi.org/project/getmem-ai/) <br>
- [getmem on npm](https://npmjs.com/package/getmem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes environment variable setup for GETMEM_API_KEY and example calls to retrieve and ingest memory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
