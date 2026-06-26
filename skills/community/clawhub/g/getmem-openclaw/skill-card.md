## Description: <br>
Adds getmem.ai persistent memory to OpenClaw by retrieving memory context before replies and ingesting user and assistant exchanges after replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimblev2023](https://clawhub.ai/user/nimblev2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this OpenClaw plugin to give agents per-user persistent memory by injecting retrieved getmem.ai context and storing completed exchanges for future retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User conversations and assistant replies may be sent to getmem.ai for persistent remote memory. <br>
Mitigation: Install only with user or administrator approval after confirming privacy, retention, deletion, and compliance requirements. <br>
Risk: Broad default memory collection can be inappropriate for regulated, secret-bearing, or policy-restricted conversations. <br>
Mitigation: Avoid those conversations unless there is an explicit policy for disabling, scoping, or approving memory use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nimblev2023/getmem-openclaw) <br>
- [getmem.ai](https://getmem.ai) <br>
- [getmem.ai API reference](https://getmem.ai/llms-full.txt) <br>
- [getmem.ai platform](https://platform.getmem.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Configuration] <br>
**Output Format:** [Plain text memory context injected into the agent prompt, with JSON API requests for memory retrieval and ingestion.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a getmem.ai API key and can be disabled with the enabled configuration flag.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
