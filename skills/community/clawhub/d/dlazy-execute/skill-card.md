## Description: <br>
Executes a sequence of dependent dLazy shapes end-to-end by resolving upstream outputs into downstream inputs and skipping shapes that are not idle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dlazyai](https://clawhub.ai/user/dlazyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run dLazy plan shapes through the dLazy CLI/API, preserving dependency order and passing producer outputs into consumer inputs. It is intended for workflows where the user already plans to authenticate with dLazy and execute hosted cloud generation tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The broad trigger can accidentally start a paid dLazy cloud workflow that sends prompts or files to dLazy. <br>
Mitigation: Narrow the invocation phrase, review each proposed command and payload before execution, and use dry-run behavior when available before starting a paid run. <br>
Risk: The skill requires a dLazy API key and may save or read credentials from local CLI configuration. <br>
Mitigation: Use a revocable dLazy key, protect the local config file, prefer least-privilege organization access, and rotate or revoke the key when no longer needed. <br>
Risk: Prompts, parameters, and referenced local media may be sent to hosted dLazy API and storage endpoints. <br>
Mitigation: Avoid confidential prompts and sensitive media unless the user has approved using dLazy for that content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dlazyai/dlazy-execute) <br>
- [dLazy homepage](https://dlazy.com) <br>
- [dLazy CLI npm package](https://www.npmjs.com/package/@dlazy/cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the CLI returns JSON execution results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Async executions may return a task identifier instead of immediate shape outputs.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
