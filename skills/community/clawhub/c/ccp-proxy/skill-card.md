## Description:

Runs a local OpenAI-compatible CCP API reverse proxy on 127.0.0.1:8257 for starting, stopping, checking, testing, and configuring access to the China Mobile CCP platform for models such as qwen-3.5.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyongjie](https://clawhub.ai/user/wangyongjie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage a persistent local proxy that forwards OpenAI-compatible chat completion requests to the CCP upstream and configures WorkBuddy to use the local endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local proxy forwards prompts and Authorization headers to the CCP upstream.

Mitigation: Use the proxy only for intended CCP workloads, prefer a limited-scope API key, and avoid sending sensitive prompts unless the upstream handling is acceptable.

Risk: The CCP API key is stored in ~/.workbuddy/models.json.

Mitigation: Check file permissions on the configuration file, avoid shared machines for sensitive keys, and rotate the key if exposure is suspected.

Risk: The proxy runs as a persistent local daemon with PID-file based service control.

Mitigation: Use the status command before start or stop, verify the PID file if service state looks stale, and review the log file when startup or shutdown behavior is unclear.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can direct local daemon control, connectivity testing, and WorkBuddy model configuration updates.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
