## Description: <br>
Use Alibaba Cloud Document Mind through the Node.js SDK to submit document parsing jobs and poll for structured text, layout, and document results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Claude Code or Codex workflows that submit document URLs or uploads to Alibaba Cloud DocMind, poll asynchronous results, and capture evidence for document understanding tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud credentials could be exposed if they are pasted into chats, logs, or saved in shared output artifacts. <br>
Mitigation: Use least-privilege, preferably short-lived Alibaba Cloud credentials and keep secrets out of prompts, logs, and evidence files. <br>
Risk: Documents submitted to DocMind may leave the local environment and be handled by Alibaba Cloud. <br>
Mitigation: Process only documents that are approved for Alibaba Cloud handling and choose the region explicitly when required by the task. <br>


## Reference(s): <br>
- [Source list](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Alibaba Cloud credentials and a bounded polling loop; results depend on DocMind service responses.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
